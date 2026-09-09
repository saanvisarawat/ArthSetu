from sqlalchemy import Column, String, Float, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from .database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    village = Column(String, index=True)
    block = Column(String)
    district = Column(String)
    state = Column(String)
    business_category = Column(String)
    margin_capital = Column(Float)
    project_cost = Column(Float, nullable=True)
    loan_amount = Column(Float, nullable=True)
    scheme_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class LocalMarketData(Base):
    __tablename__ = "local_market_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    village_name = Column(String, unique=True, index=True)
    population = Column(Integer)
    nearby_market = Column(String)