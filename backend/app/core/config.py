"""
Application configuration settings
Loads configuration from environment variables
"""
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import List, Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "National Strategy Transparency Platform"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    
    # Security
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    MFA_ISSUER_NAME: str = "NSTP"
    
    # Password Policy
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_DIGITS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True
    PASSWORD_EXPIRY_DAYS: int = 90
    MAX_LOGIN_ATTEMPTS: int = 5
    ACCOUNT_LOCKOUT_DURATION_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS
    CORS_ORIGINS: Optional[List[str]] = None
    ALLOWED_HOSTS: Optional[List[str]] = None
    
    @validator("CORS_ORIGINS", pre=True, always=True)
    def assemble_cors_origins(cls, v):
        if v is None or v == "":
            return ["http://localhost:3000"]
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["http://localhost:3000"]
    
    @validator("ALLOWED_HOSTS", pre=True, always=True)
    def assemble_allowed_hosts(cls, v):
        if v is None or v == "":
            return ["*"]
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        elif isinstance(v, list):
            return v
        return ["*"]
    
    # AWS S3
    USE_S3: bool = True
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "eu-west-1"
    AWS_S3_BUCKET: Optional[str] = None
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 52428800  # 50MB
    ALLOWED_DOCUMENT_EXTENSIONS: Optional[List[str]] = None
    ALLOWED_IMAGE_EXTENSIONS: Optional[List[str]] = None
    UPLOAD_DIR: str = "./uploads"
    
    @validator("ALLOWED_DOCUMENT_EXTENSIONS", pre=True, always=True)
    def split_document_extensions(cls, v):
        if v is None or v == "":
            return [".pdf"]
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        elif isinstance(v, list):
            return v
        return [".pdf"]
    
    @validator("ALLOWED_IMAGE_EXTENSIONS", pre=True, always=True)
    def split_image_extensions(cls, v):
        if v is None or v == "":
            return [".jpg", ".jpeg", ".png"]
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        elif isinstance(v, list):
            return v
        return [".jpg", ".jpeg", ".png"]
    
    # Email
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_TLS: bool = True
    EMAIL_FROM: str
    EMAIL_FROM_NAME: str = "National Strategy Platform"
    EMAIL_REPLY_TO: Optional[str] = None
    SEND_EMAIL_NOTIFICATIONS: bool = True
    
    # Notifications
    UPDATE_REMINDER_DAYS: int = 7
    OVERDUE_ESCALATION_DAYS: int = 7
    QUESTION_RESPONSE_DAYS: int = 14
    
    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Session
    SESSION_TIMEOUT_MINUTES: int = 30
    MAX_CONCURRENT_SESSIONS: int = 2
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # Feature Flags
    ENABLE_Q_AND_A: bool = True
    ENABLE_FILE_UPLOADS: bool = True
    ENABLE_EMAIL_NOTIFICATIONS: bool = True
    ENABLE_MFA: bool = True
    REQUIRE_MFA_FOR_ADMINS: bool = True
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    ENABLE_METRICS: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
Path("./logs").mkdir(parents=True, exist_ok=True)
