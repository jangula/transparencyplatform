"""
User model
Represents all system users (Strategy Owners, Ministry Admins, Platform Admins)
"""
from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from app.db.base import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    STRATEGY_OWNER = "STRATEGY_OWNER"
    MINISTRY_ADMIN = "MINISTRY_ADMIN"
    PLATFORM_ADMIN = "PLATFORM_ADMIN"


class User(Base):
    """User database model"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), nullable=False, index=True)
    
    # Ministry relationship
    ministry_id = Column(UUID(as_uuid=True), ForeignKey("ministries.id"), nullable=True)
    
    # Account status
    is_active = Column(Boolean, default=True, nullable=False)
    
    # MFA
    mfa_enabled = Column(Boolean, default=False, nullable=False)
    mfa_secret = Column(String(255), nullable=True)  # Encrypted TOTP secret
    
    # Login tracking
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)
    last_login = Column(DateTime, nullable=True)
    
    # Password management
    password_changed_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    password_expires_at = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    ministry = relationship("Ministry", back_populates="users")
    owned_strategies = relationship("Strategy", back_populates="owner", foreign_keys="Strategy.owner_id")
    # progress_updates = relationship("ProgressUpdate", back_populates="user")
    # responses = relationship("Response", back_populates="user")
    # audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_locked(self) -> bool:
        """Check if account is locked"""
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False
    
    @property
    def password_expired(self) -> bool:
        """Check if password has expired"""
        if self.password_expires_at and self.password_expires_at < datetime.utcnow():
            return True
        return False
