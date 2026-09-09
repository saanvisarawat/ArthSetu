from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional
from typing import Dict, Any

class UserCreate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    language_pref: str = "en"

class UserResponse(UserCreate):
    id: UUID
    created_at: datetime

class ProjectCreate(BaseModel):
    village: str
    block: str
    district: str
    state: str
    business_category: str
    margin_capital: float
    project_cost: Optional[float] = None
    loan_amount: Optional[float] = None
    scheme_type: Optional[str] = None


class ProjectResponse(ProjectCreate):
    id: UUID
    created_at: datetime   

class FeasibilityReportResponse(BaseModel):
    project_id: UUID
    status: str
    language: str
    market_reach_json: Dict[str, Any]
    opportunity_json: Dict[str, Any]
    swot_json: Dict[str, Any]
    threats_json: Dict[str, Any]
    competitor_json: Dict[str, Any]
    pricing_json: Dict[str, Any]