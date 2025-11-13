"""
Question and Response models
Represents citizen questions and government responses
"""
from sqlalchemy import Column, String, Text, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db.base import Base


class QuestionStatus(str, enum.Enum):
    """Question status enumeration"""
    PENDING_MODERATION = "PENDING_MODERATION"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"


class Question(Base):
    """Question database model"""
    
    __tablename__ = "questions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=False, index=True)
    
    # Submitter information (optional, encrypted)
    submitter_name = Column(String(255), nullable=True)
    submitter_email = Column(String(255), nullable=True)  # Encrypted in application layer
    
    # Question content
    question_text = Column(Text, nullable=False)
    
    # Moderation
    status = Column(Enum(QuestionStatus), default=QuestionStatus.PENDING_MODERATION, nullable=False, index=True)
    moderation_notes = Column(Text, nullable=True)
    moderated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    moderated_at = Column(DateTime, nullable=True)
    
    # Timestamps
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    strategy = relationship("Strategy", back_populates="questions")
    moderator = relationship("User", foreign_keys=[moderated_by])
    responses = relationship("Response", back_populates="question", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Question {self.id} - {self.status}>"
    
    @property
    def is_answered(self) -> bool:
        """Check if question has been answered"""
        return len(self.responses) > 0
    
    @property
    def display_name(self) -> str:
        """Get display name for submitter"""
        return self.submitter_name if self.submitter_name else "Anonymous Citizen"


class Response(Base):
    """Response database model"""
    
    __tablename__ = "responses"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    question_id = Column(UUID(as_uuid=True), ForeignKey("questions.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    response_text = Column(Text, nullable=False)
    
    # Timestamps
    published_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    question = relationship("Question", back_populates="responses")
    # user = relationship("User", back_populates="responses")
    user = relationship("User")
    
    def __repr__(self):
        return f"<Response to Question {self.question_id}>"
