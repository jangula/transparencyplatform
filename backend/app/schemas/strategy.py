"""
Strategy Pydantic schemas
"""
from pydantic import BaseModel, UUID4, validator
from typing import Optional, List
from datetime import datetime, date
from app.models.strategy import StrategyStatus, StrategySector as Sector, NDPPillar


class StrategyBase(BaseModel):
    """Base strategy schema"""
    title: str
    description: str
    sector: Sector
    ndp_pillar: Optional[NDPPillar] = None
    
    @validator('title')
    def title_length(cls, v):
        if len(v) > 200:
            raise ValueError('Title must be 200 characters or less')
        return v


class StrategyCreate(StrategyBase):
    """Schema for creating a strategy"""
    ministry_id: UUID4
    owner_id: UUID4
    announcement_date: date
    start_date: date
    end_date: date
    budget_allocated: Optional[float] = None
    regions_affected: Optional[List[str]] = None
    document_url: Optional[str] = None
    
    @validator('end_date')
    def end_after_start(cls, v, values):
        if 'start_date' in values and v <= values['start_date']:
            raise ValueError('End date must be after start date')
        return v


class StrategyUpdate(BaseModel):
    """Schema for updating a strategy"""
    title: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[UUID4] = None
    status: Optional[StrategyStatus] = None
    budget_allocated: Optional[float] = None
    regions_affected: Optional[List[str]] = None
    document_url: Optional[str] = None


class Strategy(StrategyBase):
    """Schema for strategy response"""
    id: UUID4
    ministry_id: UUID4
    owner_id: UUID4
    document_url: Optional[str]
    announcement_date: date
    start_date: date
    end_date: date
    budget_allocated: Optional[float]
    regions_affected: Optional[List[str]] = None
    status: StrategyStatus
    visibility: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StrategyWithDetails(Strategy):
    """Strategy with additional details"""
    ministry_name: Optional[str] = None
    ministry_abbreviation: Optional[str] = None
    owner_name: Optional[str] = None
    total_milestones: int = 0
    completed_milestones: int = 0
    overall_completion: float = 0.0
    last_update_date: Optional[datetime] = None
    latest_status: Optional[str] = None  # GREEN, AMBER, RED


class StrategyList(BaseModel):
    """Schema for paginated strategy list"""
    strategies: List[Strategy]
    total: int
    page: int
    page_size: int


class StrategyStats(BaseModel):
    """Strategy statistics"""
    total: int
    active: int
    completed: int
    suspended: int
    on_track: int  # GREEN status
    with_challenges: int  # AMBER status
    delayed: int  # RED status
