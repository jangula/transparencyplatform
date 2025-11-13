"""
Milestone model
Represents milestones within a strategy
"""
from sqlalchemy import Column, String, Text, Date, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db.base import Base


class MilestoneStatus(str, enum.Enum):
    """Milestone status enumeration"""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    DELAYED = "DELAYED"


class Milestone(Base):
    """Milestone database model"""
    
    __tablename__ = "milestones"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=False, index=True)
    
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    target_date = Column(Date, nullable=False)
    responsible_officer = Column(String(255), nullable=True)
    kpi = Column(String(500), nullable=True)  # Key Performance Indicator
    
    status = Column(Enum(MilestoneStatus), default=MilestoneStatus.NOT_STARTED, nullable=False)
    completion_percentage = Column(Integer, default=0, nullable=False)  # 0-100
    order_index = Column(Integer, nullable=False)  # For display ordering
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    strategy = relationship("Strategy", back_populates="milestones")
    # milestone_updates = relationship("MilestoneUpdate", back_populates="milestone", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Milestone {self.title} ({self.status})>"
    
    @property
    def is_overdue(self) -> bool:
        """Check if milestone is overdue"""
        if self.status != MilestoneStatus.COMPLETED:
            return datetime.now().date() > self.target_date
        return False
