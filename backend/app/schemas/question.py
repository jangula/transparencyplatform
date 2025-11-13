"""
Pydantic schemas for questions and responses
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.models.question import QuestionStatus


class QuestionBase(BaseModel):
    """Base schema for questions"""
    question_text: str = Field(..., max_length=500)
    submitter_name: Optional[str] = Field(None, max_length=100)
    submitter_email: Optional[EmailStr] = None


class QuestionCreate(QuestionBase):
    """Schema for creating a question"""
    strategy_id: UUID


class QuestionUpdate(BaseModel):
    """Schema for updating a question"""
    status: Optional[QuestionStatus] = None
    moderation_notes: Optional[str] = None


class QuestionResponse(QuestionBase):
    """Schema for question response"""
    id: UUID
    strategy_id: UUID
    status: QuestionStatus
    submitted_at: datetime
    moderated_at: Optional[datetime] = None
    moderated_by: Optional[UUID] = None
    moderation_notes: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuestionList(BaseModel):
    """Schema for paginated list of questions"""
    questions: List[QuestionResponse]
    total: int
    page: int
    page_size: int


class ResponseBase(BaseModel):
    """Base schema for responses"""
    response_text: str


class ResponseCreate(ResponseBase):
    """Schema for creating a response"""
    pass


class ResponseResponse(ResponseBase):
    """Schema for response response"""
    id: UUID
    question_id: UUID
    user_id: UUID
    published_at: datetime
    
    class Config:
        from_attributes = True


class QuestionWithResponse(QuestionResponse):
    """Schema for question with its response"""
    response: Optional[ResponseResponse] = None
