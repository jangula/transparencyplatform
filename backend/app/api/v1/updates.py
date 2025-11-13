"""
API endpoints for progress updates
Handles CRUD operations for strategy progress updates
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.deps import get_db, get_current_user, require_strategy_owner, require_admin
from app.models.user import User
from app.schemas.progress_update import (
    ProgressUpdateCreate,
    ProgressUpdateUpdate,
    ProgressUpdateResponse,
    ProgressUpdateList
)
from app.crud.crud_progress_update import crud_progress_update
from app.crud.crud_strategy import crud_strategy

router = APIRouter()


@router.get("/", response_model=ProgressUpdateList)
def list_progress_updates(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    strategy_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    List all progress updates (with optional filters)
    Public endpoint
    """
    if strategy_id:
        updates = crud_progress_update.get_by_strategy(db, strategy_id=strategy_id)
    else:
        updates = crud_progress_update.get_multi(db, skip=skip, limit=limit)
    
    total = len(updates) if strategy_id else crud_progress_update.count(db)
    
    return {
        "updates": updates,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "page_size": limit
    }


@router.get("/{update_id}", response_model=ProgressUpdateResponse)
def get_progress_update(
    update_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific progress update by ID"""
    update = crud_progress_update.get(db, id=update_id)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress update not found"
        )
    return update


@router.get("/strategy/{strategy_id}", response_model=List[ProgressUpdateResponse])
def get_strategy_updates(
    strategy_id: UUID,
    db: Session = Depends(get_db)
):
    """Get all progress updates for a specific strategy"""
    # Verify strategy exists
    strategy = crud_strategy.get(db, id=strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    updates = crud_progress_update.get_by_strategy(db, strategy_id=strategy_id)
    return updates


@router.post("/", response_model=ProgressUpdateResponse, status_code=status.HTTP_201_CREATED)
def create_progress_update(
    update_in: ProgressUpdateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new progress update
    Requires authentication - Strategy Owner or Admin
    """
    # Verify strategy exists
    strategy = crud_strategy.get(db, id=update_in.strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Check if user is strategy owner or admin
    from app.models.enums import UserRole
    if current_user.role not in [UserRole.PLATFORM_ADMIN, UserRole.MINISTRY_ADMIN]:
        if strategy.owner_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this strategy"
            )
    
    update = crud_progress_update.create(
        db,
        strategy_id=update_in.strategy_id,
        user_id=current_user.id,
        update_period=update_in.update_period,
        overall_status=update_in.overall_status,
        completion_percentage=update_in.completion_percentage,
        achievements=update_in.achievements,
        challenges=update_in.challenges,
        mitigation_measures=update_in.mitigation_measures,
        next_steps=update_in.next_steps,
        evidence_urls=update_in.evidence_urls or []
    )
    
    return update


@router.put("/{update_id}", response_model=ProgressUpdateResponse)
def update_progress_update(
    update_id: UUID,
    update_in: ProgressUpdateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing progress update
    Only creator or admin can update
    """
    existing_update = crud_progress_update.get(db, id=update_id)
    if not existing_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress update not found"
        )
    
    # Check permissions
    from app.models.enums import UserRole
    if current_user.role not in [UserRole.PLATFORM_ADMIN, UserRole.MINISTRY_ADMIN]:
        if existing_update.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this progress update"
            )
    
    update_data = update_in.dict(exclude_unset=True)
    updated = crud_progress_update.update(db, db_obj=existing_update, obj_in=update_data)
    
    return updated


@router.delete("/{update_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_progress_update(
    update_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a progress update
    Admin only
    """
    update = crud_progress_update.get(db, id=update_id)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progress update not found"
        )
    
    crud_progress_update.remove(db, id=update_id)
    return None


@router.get("/overdue/list", response_model=List[dict])
def list_overdue_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    List all strategies with overdue updates
    Admin only
    """
    overdue = crud_progress_update.get_overdue_strategies(db)
    return overdue
