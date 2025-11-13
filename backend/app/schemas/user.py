"""
User Pydantic schemas
"""
from pydantic import BaseModel, EmailStr, UUID4, validator
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    first_name: str
    last_name: str


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str
    role: UserRole
    ministry_id: Optional[UUID4] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 12:
            raise ValueError('Password must be at least 12 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in v):
            raise ValueError('Password must contain special character')
        return v


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    ministry_id: Optional[UUID4] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    """Base schema for user in database"""
    id: UUID4
    role: UserRole
    ministry_id: Optional[UUID4]
    is_active: bool
    mfa_enabled: bool
    is_locked: bool
    last_login: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class User(UserInDBBase):
    """Schema for user response"""
    pass


class UserWithMinistry(UserInDBBase):
    """User with ministry information"""
    ministry_name: Optional[str] = None
    ministry_abbreviation: Optional[str] = None


class UserList(BaseModel):
    """Schema for paginated user list"""
    total: int
    users: list[User]
    page: int
    page_size: int
