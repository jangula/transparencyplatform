"""
Common Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, Any


class Message(BaseModel):
    """Generic message response"""
    message: str


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Success response schema"""
    success: bool
    message: str
    data: Optional[Any] = None


class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = 1
    page_size: int = 20
    
    def get_skip(self) -> int:
        """Calculate skip value"""
        return (self.page - 1) * self.page_size
    
    def get_limit(self) -> int:
        """Get limit value"""
        return self.page_size


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    app: str
    version: str
    environment: str


class DatabaseHealth(BaseModel):
    """Database health check"""
    status: str
    database: str
    error: Optional[str] = None
