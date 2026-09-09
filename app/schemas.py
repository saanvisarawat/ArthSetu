from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from uuid import UUID

# --- User Schemas ---
class UserCreate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    language_pref: str = "en"

class UserResponse(UserCreate):
    id: UUID
    created_at: datetime

# --- Project Schemas ---
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

# --- Feasibility Report Inner Structures ---
class MarketReach(BaseModel):
    population_reached: int
    addressable_spend_inr: int
    top_channels: List[str]

class Niche(BaseModel):
    niche: str
    rationale: str

class Opportunity(BaseModel):
    top_niches: List[Niche]

class SWOT(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]

class Risk(BaseModel):
    threat: str
    mitigation: str

class Threats(BaseModel):
    risks: List[Risk]

class Competitor(BaseModel):
    estimated_count: int
    saturation_label: str
    confidence: str

class Pricing(BaseModel):
    recommended_band: str
    rationale: str

# --- Feasibility Report Main Schema ---
class FeasibilityReportResponse(BaseModel):
    project_id: str
    status: str
    language: str
    market_reach_json: MarketReach
    opportunity_json: Opportunity
    swot_json: SWOT
    threats_json: Threats
    competitor_json: Competitor
    pricing_json: Pricing