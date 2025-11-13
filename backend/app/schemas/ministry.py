"""
Ministry Pydantic schemas
"""
from pydantic import BaseModel, UUID4, HttpUrl
from typing import Optional
from datetime import datetime


class MinistryBase(BaseModel):
    """Base ministry schema"""
    name: str
    abbreviation: str
    website: Optional[HttpUrl] = None


class MinistryCreate(MinistryBase):
    """Schema for creating a ministry"""
    pass


class MinistryUpdate(BaseModel):
    """Schema for updating a ministry"""
    name: Optional[str] = None
    abbreviation: Optional[str] = None
    website: Optional[HttpUrl] = None


class Ministry(MinistryBase):
    """Schema for ministry response"""
    id: UUID4
    created_at: datetime
    
    class Config:
        from_attributes = True


class MinistryWithStats(Ministry):
    """Ministry with statistics"""
    total_strategies: int = 0
    active_strategies: int = 0
    total_users: int = 0


class MinistryList(BaseModel):
    """Schema for ministry list"""
    ministries: list[Ministry]
    total: int
