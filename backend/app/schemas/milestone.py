"""
Pydantic schemas for Milestone model
"""
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import date
from enum import Enum
from uuid import UUID


class MilestoneStatus(str, Enum):
    """Milestone status enumeration"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DELAYED = "DELAYED"


class MilestoneBase(BaseModel):
    """Base milestone schema"""
    title: str = Field(..., max_length=200, description="Milestone title")
    description: Optional[str] = Field(None, description="Detailed description")
    target_date: date = Field(..., description="Target completion date")
    responsible_officer: str = Field(..., max_length=200, description="Officer responsible")
    kpi: Optional[str] = Field(None, max_length=500, description="Key Performance Indicator")
    order_index: int = Field(..., ge=0, description="Display order")


class MilestoneCreate(MilestoneBase):
    """Schema for creating a milestone"""
    strategy_id: UUID = Field(..., description="Strategy this milestone belongs to")
    status: MilestoneStatus = Field(default=MilestoneStatus.NOT_STARTED)
    completion_percentage: int = Field(default=0, ge=0, le=100)


class MilestoneUpdate(BaseModel):
    """Schema for updating a milestone"""
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    target_date: Optional[date] = None
    responsible_officer: Optional[str] = Field(None, max_length=200)
    kpi: Optional[str] = Field(None, max_length=500)
    status: Optional[MilestoneStatus] = None
    completion_percentage: Optional[int] = Field(None, ge=0, le=100)
    order_index: Optional[int] = Field(None, ge=0)

    @validator('completion_percentage')
    def validate_completion(cls, v, values):
        """Auto-set status based on completion percentage"""
        if v is not None:
            if v == 0:
                values['status'] = MilestoneStatus.NOT_STARTED
            elif v == 100:
                values['status'] = MilestoneStatus.COMPLETED
            elif v > 0:
                values['status'] = MilestoneStatus.IN_PROGRESS
        return v


class MilestoneInDB(MilestoneBase):
    """Milestone schema as stored in database"""
    id: UUID
    strategy_id: UUID
    status: MilestoneStatus
    completion_percentage: int

    class Config:
        from_attributes = True


class Milestone(MilestoneInDB):
    """Complete milestone schema for API responses"""
    pass


class MilestoneList(BaseModel):
    """Paginated list of milestones"""
    items: list[Milestone]
    total: int
    page: int
    size: int
    pages: int
