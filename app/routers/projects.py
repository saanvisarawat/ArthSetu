from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(prefix="/api/v1/projects", tags=["Projects"])

# 1. Update the Pydantic schema to match our database columns
class ProjectInput(BaseModel):
    village: str
    block: str
    district: str
    state: str
    business_category: str
    margin_capital: float

@router.post("/")
def create_project(project: ProjectInput, db: Session = Depends(get_db)):
    # 2. Map the incoming JSON data to our SQLAlchemy model
    new_project = models.Project(
        village=project.village,
        block=project.block,
        district=project.district,
        state=project.state,
        business_category=project.business_category,
        margin_capital=project.margin_capital
    )
    
    # 3. Add to the session and commit to Supabase
    db.add(new_project)
    db.commit()
    
    # 4. Refresh to grab the auto-generated UUID from the database
    db.refresh(new_project)
    
    return {
        "message": "Project successfully saved to Supabase!", 
        "project_id": str(new_project.id)
    }

@router.get("/{project_id}")
def get_project(project_id: str, db: Session = Depends(get_db)):
    # Search the database for this specific ID
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