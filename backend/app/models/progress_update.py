"""
Progress Update models
Represents quarterly progress updates and milestone updates
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, Enum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db.base import Base


class OverallStatus(str, enum.Enum):
    """Overall status enumeration (Traffic Light)"""
    GREEN = "GREEN"  # On track
    AMBER = "AMBER"   # Minor challenges
    RED = "RED"       # Major delays/issues


class ProgressUpdate(Base):
    """Progress Update database model"""
    
    __tablename__ = "progress_updates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    
    update_period = Column(String(50), nullable=False)  # e.g., "Q3 2025"
    overall_status = Column(Enum(OverallStatus), nullable=False, index=True)
    completion_percentage = Column(Integer, nullable=False)  # 0-100
    
    # Update content
    achievements = Column(Text, nullable=False)
    challenges = Column(Text, nullable=True)
    mitigation_measures = Column(Text, nullable=True)
    next_steps = Column(Text, nullable=True)
    
    # Evidence files (S3 URLs)
    evidence_urls = Column(ARRAY(String), nullable=True)
    
    # Timestamps
    published_date = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    # strategy = relationship("Strategy", back_populates="progress_updates")
    strategy = relationship("Strategy")
    # user = relationship("User", back_populates="progress_updates")
    user = relationship("User")
    milestone_updates = relationship("MilestoneUpdate", back_populates="progress_update", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ProgressUpdate {self.update_period} - {self.overall_status}>"


class MilestoneUpdate(Base):
    """
    Links progress updates to specific milestones
    Tracks milestone-level progress within a broader update
    """
    
    __tablename__ = "milestone_updates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    progress_update_id = Column(UUID(as_uuid=True), ForeignKey("progress_updates.id"), nullable=False, index=True)
    milestone_id = Column(UUID(as_uuid=True), ForeignKey("milestones.id"), nullable=False, index=True)
    
    status = Column(String(50), nullable=False)  # Milestone status at time of update
    completion_percentage = Column(Integer, nullable=False)  # 0-100
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    progress_update = relationship("ProgressUpdate", back_populates="milestone_updates")
    # milestone = relationship("Milestone", back_populates="milestone_updates")
    milestone = relationship("Milestone")
    
    def __repr__(self):
        return f"<MilestoneUpdate {self.milestone_id} - {self.completion_percentage}%>"
