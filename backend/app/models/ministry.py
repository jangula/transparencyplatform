"""
Ministry model
Represents government ministries
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class Ministry(Base):
    """Ministry database model"""
    
    __tablename__ = "ministries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    abbreviation = Column(String(20), nullable=False, unique=True)
    website = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    users = relationship("User", back_populates="ministry", cascade="all, delete-orphan")
    strategies = relationship("Strategy", back_populates="ministry", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Ministry {self.abbreviation}: {self.name}>"
