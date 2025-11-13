"""Initialize database tables"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.db.session import engine
from app.db.base import Base

# Import all models to ensure they're registered with Base
from app.models.ministry import Ministry
from app.models.user import User
from app.models.strategy import Strategy
from app.models.milestone import Milestone
from app.models.progress_update import ProgressUpdate
from app.models.question import Question
from app.models.audit_log import AuditLog

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")
