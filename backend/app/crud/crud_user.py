"""
CRUD operations for User model
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import uuid

from app.models.user import User, UserRole
from app.core.security import get_password_hash, verify_password


class CRUDUser:
    """CRUD operations for User"""
    
    def get(self, db: Session, user_id: uuid.UUID) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        ministry_id: Optional[uuid.UUID] = None
    ) -> List[User]:
        """Get multiple users with pagination"""
        query = db.query(User)
        if ministry_id:
            query = query.filter(User.ministry_id == ministry_id)
        return query.offset(skip).limit(limit).all()
    
    def create(self, db: Session, email: str, password: str, first_name: str,
               last_name: str, role: UserRole, ministry_id: Optional[uuid.UUID] = None) -> User:
        """Create new user"""
        user = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            role=role,
            ministry_id=ministry_id,
            is_active=True,
            mfa_enabled=False,
            failed_login_attempts=0,
            password_changed_at=datetime.utcnow(),
            password_expires_at=datetime.utcnow() + timedelta(days=90)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update(self, db: Session, user_id: uuid.UUID, **kwargs) -> Optional[User]:
        """Update user"""
        user = self.get(db, user_id)
        if not user:
            return None
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def delete(self, db: Session, user_id: uuid.UUID) -> bool:
        """Soft delete user (deactivate)"""
        user = self.get(db, user_id)
        if not user:
            return False
        user.is_active = False
        db.commit()
        return True
    
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not user.is_active:
            return None
        if user.is_locked:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user
    
    def increment_failed_login(self, db: Session, user_id: uuid.UUID) -> None:
        """Increment failed login attempts"""
        user = self.get(db, user_id)
        if user:
            user.failed_login_attempts += 1
            db.commit()
    
    def lock_account(self, db: Session, user_id: uuid.UUID, minutes: int = 30) -> None:
        """Lock user account"""
        user = self.get(db, user_id)
        if user:
            user.is_locked = True
            user.locked_until = datetime.utcnow() + timedelta(minutes=minutes)
            db.commit()
    
    def unlock_account(self, db: Session, user_id: uuid.UUID) -> None:
        """Unlock user account"""
        user = self.get(db, user_id)
        if user:
            user.is_locked = False
            user.locked_until = None
            db.commit()
    
    def reset_failed_login(self, db: Session, user_id: uuid.UUID) -> None:
        """Reset failed login attempts"""
        user = self.get(db, user_id)
        if user:
            user.failed_login_attempts = 0
            db.commit()
    
    def update_last_login(self, db: Session, user_id: uuid.UUID) -> None:
        """Update last login timestamp"""
        user = self.get(db, user_id)
        if user:
            user.last_login = datetime.utcnow()
            db.commit()
    
    def update_mfa_secret(self, db: Session, user_id: uuid.UUID, secret: str) -> None:
        """Update MFA secret"""
        user = self.get(db, user_id)
        if user:
            user.mfa_secret = secret
            db.commit()
    
    def enable_mfa(self, db: Session, user_id: uuid.UUID) -> None:
        """Enable MFA for user"""
        user = self.get(db, user_id)
        if user:
            user.mfa_enabled = True
            db.commit()
    
    def disable_mfa(self, db: Session, user_id: uuid.UUID) -> None:
        """Disable MFA for user"""
        user = self.get(db, user_id)
        if user:
            user.mfa_enabled = False
            user.mfa_secret = None
            db.commit()
    
    def update_password(self, db: Session, user_id: uuid.UUID, new_password: str) -> None:
        """Update user password"""
        user = self.get(db, user_id)
        if user:
            user.password_hash = get_password_hash(new_password)
            user.password_changed_at = datetime.utcnow()
            user.password_expires_at = datetime.utcnow() + timedelta(days=90)
            db.commit()
    
    def check_password_expired(self, db: Session, user_id: uuid.UUID) -> bool:
        """Check if password has expired"""
        user = self.get(db, user_id)
        if not user:
            return True
        if not user.password_expires_at:
            return False
        return datetime.utcnow() > user.password_expires_at


crud_user = CRUDUser()
