"""
Dependency injection for FastAPI routes
Authentication, database session, etc.
"""
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.core.security import decode_token
from app.models.user import User
from app.crud import crud_user


# HTTP Bearer token security
security = HTTPBearer()


def get_db() -> Generator:
    """
    Dependency for database session
    Yields a database session and closes it after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Get current authenticated user from JWT token
    """
    token = credentials.credentials
    
    # Decode token
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check token type
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user ID from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Fetch user from database
    user = crud_user.get(db, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify user is active"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify user has admin role (Ministry Admin or Platform Admin)"""
    if current_user.role not in ["MINISTRY_ADMIN", "PLATFORM_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Admin access required."
        )
    return current_user


async def get_current_platform_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify user has platform admin role"""
    if current_user.role != "PLATFORM_ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Platform admin access required."
        )
    return current_user


# Alias for backwards compatibility
require_admin = get_current_platform_admin


async def get_current_strategy_owner(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify user is a strategy owner"""
    if current_user.role not in ["STRATEGY_OWNER", "MINISTRY_ADMIN", "PLATFORM_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions. Strategy owner access required."
        )
    return current_user


# Alias for backwards compatibility
require_strategy_owner = get_current_strategy_owner


def check_user_ministry_access(user: User, ministry_id: str) -> bool:
    """Check if user has access to specific ministry"""
    # Platform admins have access to all ministries
    if user.role == "PLATFORM_ADMIN":
        return True
    
    # Other users can only access their own ministry
    return str(user.ministry_id) == ministry_id


def check_user_strategy_access(user: User, strategy_owner_id: str, ministry_id: str) -> bool:
    """Check if user has access to specific strategy"""
    # Platform admins have access to all strategies
    if user.role == "PLATFORM_ADMIN":
        return True
    
    # Strategy owners can access their own strategies
    if str(user.id) == strategy_owner_id:
        return True
    
    # Ministry admins can access strategies in their ministry
    if user.role == "MINISTRY_ADMIN" and str(user.ministry_id) == ministry_id:
        return True
    
    return False
