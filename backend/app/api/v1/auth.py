"""
Authentication endpoints
Login, register, MFA, password management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.core.deps import get_db, get_current_user
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    validate_password_strength,
    generate_mfa_secret,
    generate_mfa_qr_code,
    verify_mfa_token,
    generate_backup_codes,
    decode_token
)
from app.core.config import settings
from app.models.user import User
from app.schemas.auth import (
    Token,
    UserLogin,
    UserCreate,
    MFASetupResponse,
    MFAVerifyRequest,
    PasswordChangeRequest
)
from app.crud import crud_user
from app.services.audit import create_audit_log

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    User login endpoint
    Returns access and refresh tokens
    """
    # Find user by email
    user = crud_user.get_by_email(db, email=credentials.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if account is locked
    if user.is_locked:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is locked. Please contact administrator."
        )
    
    # Check if account is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        # Increment failed login attempts
        crud_user.increment_failed_login(db, user_id=user.id)
        
        # Lock account if too many failed attempts
        if user.failed_login_attempts >= settings.MAX_LOGIN_ATTEMPTS:
            crud_user.lock_account(db, user_id=user.id, minutes=settings.ACCOUNT_LOCKOUT_DURATION_MINUTES)
        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Check if MFA is enabled (for now, skip MFA check via form data)
    # MFA can be handled via a separate request header if needed
    
    # Check if password has expired
    if user.password_expired:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password has expired. Please change your password.",
            headers={"X-Password-Expired": "true"}
        )
    
    # Reset failed login attempts
    crud_user.reset_failed_login(db, user_id=user.id)
    
    # Update last login
    crud_user.update_last_login(db, user_id=user.id)
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Create audit log
    create_audit_log(
        db=db,
        user_id=user.id,
        action="USER_LOGIN",
        entity_type="User",
        entity_id=user.id,
        metadata={"email": user.email}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "ministry_id": str(user.ministry_id) if user.ministry_id else None
        }
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    payload = decode_token(refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    user = crud_user.get(db, id=user_id)
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )
    
    # Create new access token
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/register", response_model=dict)
async def register(
    user_create: UserCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Register new user (admin only)
    """
    # Only admins can create users
    if current_user.role not in ["MINISTRY_ADMIN", "PLATFORM_ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Validate password strength
    is_valid, error_msg = validate_password_strength(user_create.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Check if user already exists
    existing_user = crud_user.get_by_email(db, email=user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = crud_user.create(db, obj_in=user_create)
    
    # Create audit log
    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="USER_CREATED",
        entity_type="User",
        entity_id=user.id,
        metadata={"created_email": user.email, "role": user.role}
    )
    
    return {
        "message": "User created successfully",
        "user_id": str(user.id),
        "email": user.email
    }


@router.post("/mfa/setup", response_model=MFASetupResponse)
async def setup_mfa(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Setup MFA for user
    Returns QR code and backup codes
    """
    # Generate MFA secret
    secret = generate_mfa_secret()
    
    # Generate QR code
    qr_code = generate_mfa_qr_code(current_user.email, secret)
    
    # Generate backup codes
    backup_codes = generate_backup_codes()
    
    # Save secret (temporarily, will be confirmed after verification)
    crud_user.update_mfa_secret(db, user_id=current_user.id, secret=secret)
    
    return {
        "secret": secret,
        "qr_code": qr_code,
        "backup_codes": backup_codes
    }


@router.post("/mfa/verify")
async def verify_mfa_setup(
    mfa_verify: MFAVerifyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Verify and enable MFA
    """
    if not current_user.mfa_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="MFA not set up. Please call /mfa/setup first"
        )
    
    # Verify token
    if not verify_mfa_token(current_user.mfa_secret, mfa_verify.token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid MFA token"
        )
    
    # Enable MFA
    crud_user.enable_mfa(db, user_id=current_user.id)
    
    # Create audit log
    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="MFA_ENABLED",
        entity_type="User",
        entity_id=current_user.id
    )
    
    return {"message": "MFA enabled successfully"}


@router.post("/password/change")
async def change_password(
    password_change: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Change user password
    """
    # Verify current password
    if not verify_password(password_change.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Validate new password strength
    is_valid, error_msg = validate_password_strength(password_change.new_password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Update password
    new_password_hash = get_password_hash(password_change.new_password)
    crud_user.update_password(db, user_id=current_user.id, password_hash=new_password_hash)
    
    # Create audit log
    create_audit_log(
        db=db,
        user_id=current_user.id,
        action="PASSWORD_CHANGED",
        entity_type="User",
        entity_id=current_user.id
    )
    
    return {"message": "Password changed successfully"}


@router.get("/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user information
    """
    return {
        "id": str(current_user.id),
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "ministry_id": str(current_user.ministry_id) if current_user.ministry_id else None,
        "is_active": current_user.is_active,
        "mfa_enabled": current_user.mfa_enabled,
        "last_login": current_user.last_login.isoformat() if current_user.last_login else None,
        "created_at": current_user.created_at.isoformat()
    }
