"""
API v1 router
Combines all API endpoints
"""
from fastapi import APIRouter

from app.api.v1 import auth, strategies, updates, questions, admin, ministries, qa, milestones, seed

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(ministries.router, prefix="/ministries", tags=["Ministries"])
api_router.include_router(strategies.router, prefix="/strategies", tags=["Strategies"])
api_router.include_router(milestones.router, prefix="/milestones", tags=["Milestones"])
api_router.include_router(updates.router, prefix="/updates", tags=["Progress Updates"])
api_router.include_router(qa.router, prefix="/questions", tags=["Questions & Answers"])
api_router.include_router(questions.router, prefix="/questions-old", tags=["Questions (Legacy)"])
api_router.include_router(admin.router, prefix="/admin", tags=["Administration"])
api_router.include_router(seed.router, prefix="/dev", tags=["Development"])
