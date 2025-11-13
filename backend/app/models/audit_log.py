"""
Audit Log model
Tracks all significant actions in the system
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.db.base import Base


class AuditLog(Base):
    """Audit Log database model"""
    
    __tablename__ = "audit_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    
    # Action details
    action = Column(String(100), nullable=False, index=True)  # e.g., "USER_LOGIN", "STRATEGY_CREATED"
    entity_type = Column(String(50), nullable=True)  # e.g., "Strategy", "User"
    entity_id = Column(UUID(as_uuid=True), nullable=True)
    
    # Request details
    ip_address = Column(String(45), nullable=True)  # IPv6 max length
    user_agent = Column(String(500), nullable=True)
    
    # Additional context (JSON)
    extra_data = Column(JSONB, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    # user = relationship("User", back_populates="audit_logs")
    user = relationship("User")
    
    def __repr__(self):
        return f"<AuditLog {self.action} by {self.user_id} at {self.timestamp}>"
