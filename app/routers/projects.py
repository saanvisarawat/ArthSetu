import json
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..services.financial_engine import run_eligibility_engine, ValidationError
from ..services.llm_engine import generate_feasibility_report

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

# 1. Schema matching incoming project creation payload
class ProjectInput(BaseModel):
    village: str
    block: str
    district: str
    state: str
    business_category: str
    margin_capital: float

@router.post("/")
def create_project(project: ProjectInput, db: Session = Depends(get_db)):
    # 2. Map incoming data to the SQLAlchemy model
    new_project = models.Project(
        village=project.village,
        block=project.block,
        district=project.district,
        state=project.state,
        business_category=project.business_category,
        margin_capital=project.margin_capital
    )
    
    # 3. Commit to database
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return {
        "message": "Project successfully saved to Supabase!", 
        "project_id": str(new_project.id)
    }

@router.get("/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    return {
        "project_id": project.id,
        "status": "Pending",
        "data": {
            "village": project.village,
            "category": project.business_category,
            "capital": project.margin_capital
        }
    }

@router.post("/{project_id}/calculate-eligibility")
def calculate_eligibility(project_id: str, db: Session = Depends(get_db)):
    # 1. Fetch project record
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2. Run Financial Structuring & Scheme Auto-Selection
    try:
        result = run_eligibility_engine(project.margin_capital)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 3. Persist computed figures back onto the project
    project.project_cost = result["project_cost"]
    project.loan_amount = result["final_loan_amount"]
    project.scheme_type = result["scheme_name"]

    db.commit()
    db.refresh(project)

    return result

@router.post("/{project_id}/generate-report")
def generate_report(project_id: str, db: Session = Depends(get_db)):
    # 1. Fetch project record
    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 2. Ensure financial calculations have been run first
    if not project.project_cost:
        raise HTTPException(
            status_code=400, 
            detail="Run eligibility calculation before generating report."
        )

    # 3. Query local market demographics for the project's village
    market_data = db.query(models.LocalMarketData).filter(
        models.LocalMarketData.village_name.ilike(project.village.strip())
    ).first()

    # Use database values if available, otherwise apply sensible defaults
    population = market_data.population if market_data else 10000
    market_access = market_data.nearby_market if market_data else "Local village weekly haat and roadside retail"

    # 4. Call LLM engine using grounded demographic and financial data
    raw_report = generate_feasibility_report(
        village=project.village,
        category=project.business_category,
        project_cost=project.project_cost,
        competitors=4,  # Baseline default
        population=population,
        market_access=market_access
    )

    # Parse to dict if string returned to ensure valid JSON response
    return json.loads(raw_report) if isinstance(raw_report, str) else raw_report