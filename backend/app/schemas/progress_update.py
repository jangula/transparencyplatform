"""
Pydantic schemas for progress updates
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from app.models.strategy import StrategyStatus


class ProgressUpdateBase(BaseModel):
    """Base schema for progress updates"""
    update_period: str = Field(..., description="Update period (e.g., Q1 2025)")
    overall_status: StrategyStatus
    completion_percentage: int = Field(..., ge=0, le=100)
    achievements: str
    challenges: Optional[str] = None
    mitigation_measures: Optional[str] = None
    next_steps: Optional[str] = None
    evidence_urls: Optional[List[str]] = Field(default_factory=list)


class ProgressUpdateCreate(ProgressUpdateBase):
    """Schema for creating a progress update"""
    strategy_id: UUID
    
    @field_validator('completion_percentage')
    @classmethod
    def validate_percentage(cls, v):
        if not 0 <= v <= 100:
            raise ValueError('Completion percentage must be between 0 and 100')
        return v


class ProgressUpdateUpdate(BaseModel):
    """Schema for updating a progress update"""
    update_period: Optional[str] = None
    overall_status: Optional[StrategyStatus] = None
    completion_percentage: Optional[int] = Field(None, ge=0, le=100)
    achievements: Optional[str] = None
    challenges: Optional[str] = None
    mitigation_measures: Optional[str] = None
    next_steps: Optional[str] = None
    evidence_urls: Optional[List[str]] = None


class ProgressUpdateResponse(ProgressUpdateBase):
    """Schema for progress update responses"""
    id: UUID
    strategy_id: UUID
    user_id: UUID
    published_date: datetime
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProgressUpdateList(BaseModel):
    """Schema for paginated progress update list"""
    updates: List[ProgressUpdateResponse]
    total: int
    page: int
    page_size: int


# Milestone Update schemas
class MilestoneUpdateBase(BaseModel):
    """Base schema for milestone updates"""
    status: StrategyStatus
    completion_percentage: int = Field(..., ge=0, le=100)
    notes: Optional[str] = None


class MilestoneUpdateCreate(MilestoneUpdateBase):
    """Schema for creating a milestone update"""
    milestone_id: UUID
    progress_update_id: UUID


class MilestoneUpdateResponse(MilestoneUpdateBase):
    """Schema for milestone update responses"""
    id: UUID
    milestone_id: UUID
    progress_update_id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True
