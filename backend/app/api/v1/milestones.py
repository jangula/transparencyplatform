"""
Milestones API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.deps import get_db, get_current_active_user
from app.crud import crud_milestone, crud_strategy
from app.schemas.milestone import (
    Milestone,
    MilestoneCreate,
    MilestoneUpdate,
    MilestoneList
)
from app.schemas.user import User
from app.models.user import UserRole

router = APIRouter()


def check_milestone_permission(current_user: User, strategy, action: str = "modify"):
    """Check if user has permission to perform action on milestone"""
    if current_user.role == UserRole.PLATFORM_ADMIN:
        return True
    
    if current_user.role == UserRole.MINISTRY_ADMIN:
        if str(strategy.ministry_id) == str(current_user.ministry_id):
            return True
    
    if current_user.role == UserRole.STRATEGY_OWNER:
        if str(strategy.owner_id) == str(current_user.id):
            return True
    
    return False


@router.post("/", response_model=Milestone, status_code=status.HTTP_201_CREATED)
def create_milestone(
    milestone_in: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new milestone"""
    strategy = crud_strategy.get(db, id=milestone_in.strategy_id)
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    
    if not check_milestone_permission(current_user, strategy):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    return crud_milestone.create(db, obj_in=milestone_in)


@router.get("/{milestone_id}", response_model=Milestone)
def get_milestone(milestone_id: UUID, db: Session = Depends(get_db)):
    """Get a specific milestone"""
    milestone = crud_milestone.get(db, id=milestone_id)
    if not milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    return milestone


@router.get("/strategy/{strategy_id}", response_model=List[Milestone])
def get_strategy_milestones(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Get all milestones for a strategy"""
    strategy = crud_strategy.get(db, id=strategy_id)
    if not strategy:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Strategy not found")
    
    return crud_milestone.get_by_strategy(db, strategy_id=strategy_id, skip=skip, limit=limit)


@router.put("/{milestone_id}", response_model=Milestone)
def update_milestone(
    milestone_id: UUID,
    milestone_in: MilestoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a milestone"""
    milestone = crud_milestone.get(db, id=milestone_id)
    if not milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    
    strategy = crud_strategy.get(db, id=milestone.strategy_id)
    if not check_milestone_permission(current_user, strategy):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    return crud_milestone.update(db, db_obj=milestone, obj_in=milestone_in)


@router.delete("/{milestone_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_milestone(
    milestone_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a milestone"""
    milestone = crud_milestone.get(db, id=milestone_id)
    if not milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    
    strategy = crud_strategy.get(db, id=milestone.strategy_id)
    if current_user.role not in [UserRole.MINISTRY_ADMIN, UserRole.PLATFORM_ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    if current_user.role == UserRole.MINISTRY_ADMIN:
        if str(strategy.ministry_id) != str(current_user.ministry_id):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    crud_milestone.remove(db, id=milestone_id)
    return None


@router.post("/{milestone_id}/reorder", response_model=Milestone)
def reorder_milestone(
    milestone_id: UUID,
    new_order: int = Query(..., ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Change the display order of a milestone"""
    milestone = crud_milestone.get(db, id=milestone_id)
    if not milestone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Milestone not found")
    
    strategy = crud_strategy.get(db, id=milestone.strategy_id)
    if not check_milestone_permission(current_user, strategy):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No permission")
    
    return crud_milestone.update(db, db_obj=milestone, obj_in={"order_index": new_order})
