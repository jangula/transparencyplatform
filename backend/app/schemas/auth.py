"""
Auth Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    mfa_token: Optional[str] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: Optional[dict] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: str
    ministry_id: Optional[str] = None

class MFASetupResponse(BaseModel):
    secret: str
    qr_code: str
    backup_codes: list[str]

class MFAVerifyRequest(BaseModel):
    token: str

class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str
