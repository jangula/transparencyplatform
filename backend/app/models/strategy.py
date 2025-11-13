"""
Strategy model
Represents government strategies/policies being tracked
"""
from sqlalchemy import Column, String, Text, Date, Numeric, DateTime, Enum, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db.base import Base


class StrategySector(str, enum.Enum):
    """Sector enumeration"""
    HEALTH = "HEALTH"
    EDUCATION = "EDUCATION"
    AGRICULTURE = "AGRICULTURE"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    ICT = "ICT"
    ENERGY = "ENERGY"
    WATER = "WATER"
    TOURISM = "TOURISM"
    MINING = "MINING"
    FINANCE = "FINANCE"
    ENVIRONMENT = "ENVIRONMENT"
    TRANSPORT = "TRANSPORT"
    HOUSING = "HOUSING"
    SOCIAL_WELFARE = "SOCIAL_WELFARE"
    JUSTICE = "JUSTICE"
    DEFENSE = "DEFENSE"
    OTHER = "OTHER"


class NDPPillar(str, enum.Enum):
    """NDP6 Pillar enumeration"""
    PILLAR_1 = "ECONOMIC_PROGRESSION"
    PILLAR_2 = "SOCIAL_TRANSFORMATION"
    PILLAR_3 = "ENVIRONMENTAL_SUSTAINABILITY"
    PILLAR_4 = "GOOD_GOVERNANCE"


class StrategyStatus(str, enum.Enum):
    """Strategy status enumeration"""
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    SUSPENDED = "SUSPENDED"


class StrategyVisibility(str, enum.Enum):
    """Strategy visibility"""
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"


class Strategy(Base):
    """Strategy database model"""
    
    __tablename__ = "strategies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(200), nullable=False, index=True)
    description = Column(Text, nullable=False)
    
    # Ministry and owner
    ministry_id = Column(UUID(as_uuid=True), ForeignKey("ministries.id"), nullable=False, index=True)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    
    # Document
    document_url = Column(String(500), nullable=True)  # S3 path or URL
    
    # Timeline
    announcement_date = Column(Date, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    
    # Budget
    budget_allocated = Column(Numeric(15, 2), nullable=True)  # In NAD
    
    # Classification
    sector = Column(Enum(StrategySector), nullable=False, index=True)
    regions_affected = Column(ARRAY(String), nullable=True)  # Array of region names
    ndp_pillar = Column(Enum(NDPPillar), nullable=True)
    
    # Status
    status = Column(Enum(StrategyStatus), default=StrategyStatus.ACTIVE, nullable=False, index=True)
    visibility = Column(Enum(StrategyVisibility), default=StrategyVisibility.PUBLIC, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    ministry = relationship("Ministry", back_populates="strategies")
    owner = relationship("User", back_populates="owned_strategies", foreign_keys=[owner_id])
    milestones = relationship("Milestone", back_populates="strategy", cascade="all, delete-orphan")
    # progress_updates = relationship("ProgressUpdate", back_populates="strategy", cascade="all, delete-orphan")
    questions = relationship("Question", back_populates="strategy", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Strategy {self.title}>"
    
    @property
    def latest_update(self):
        """Get the most recent progress update"""
        # if self.progress_updates:
        #     return sorted(self.progress_updates, key=lambda x: x.published_date, reverse=True)[0]
        return None
    
    @property
    def overall_completion(self) -> int:
        """Calculate overall completion percentage"""
        latest = self.latest_update
        if latest:
            return latest.completion_percentage
        return 0
