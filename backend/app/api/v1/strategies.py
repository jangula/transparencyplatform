"""
Strategy API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.core.deps import get_db, get_current_user, require_admin, get_current_active_user
from app.crud.crud_strategy import crud_strategy
from app.schemas.strategy import (
    Strategy, StrategyCreate, StrategyUpdate, StrategyList, StrategyStats,
    StrategyWithDetails
)
from app.schemas.common import Message
from app.models.user import User, UserRole
from app.models.strategy import StrategyStatus, StrategySector

router = APIRouter()


@router.get("/", response_model=StrategyList)
def list_strategies(
    skip: int = 0,
    limit: int = 20,
    ministry_id: Optional[UUID] = None,
    status: Optional[StrategyStatus] = None,
    sector: Optional[StrategySector] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get list of strategies with filters (public endpoint)
    """
    if search:
        strategies = crud_strategy.search(db, search, skip=skip, limit=limit)
        total = len(strategies)  # Simplified for now
    else:
        strategies = crud_strategy.get_multi(
            db, 
            skip=skip, 
            limit=limit,
            ministry_id=ministry_id,
            status=status,
            sector=sector
        )
        total = crud_strategy.get_active_count(db)
    
    return StrategyList(
        strategies=strategies,
        total=total,
        page=skip // limit + 1,
        page_size=limit
    )


@router.get("/stats", response_model=StrategyStats)
def get_strategy_stats(db: Session = Depends(get_db)):
    """
    Get strategy statistics (public endpoint)
    """
    stats = crud_strategy.get_statistics(db)
    return StrategyStats(
        total=stats['total'],
        active=stats['active'],
        completed=stats['completed'],
        suspended=stats['suspended'],
        on_track=0,  # TODO: Calculate from updates
        with_challenges=0,
        delayed=0
    )


@router.get("/{strategy_id}", response_model=Strategy)
def get_strategy(
    strategy_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get strategy by ID (public endpoint)
    """
    strategy = crud_strategy.get(db, strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    return strategy


@router.post("/", response_model=Strategy)
def create_strategy(
    strategy_in: StrategyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new strategy (authenticated users)
    """
    # Only admins or ministry admins can create strategies
    if current_user.role not in [UserRole.PLATFORM_ADMIN, UserRole.MINISTRY_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create strategies"
        )
    
    strategy = crud_strategy.create(
        db,
        title=strategy_in.title,
        description=strategy_in.description,
        ministry_id=strategy_in.ministry_id,
        owner_id=strategy_in.owner_id,
        announcement_date=strategy_in.announcement_date,
        start_date=strategy_in.start_date,
        end_date=strategy_in.end_date,
        sector=strategy_in.sector,
        ndp_pillar=strategy_in.ndp_pillar,
        document_url=strategy_in.document_url,
        budget_allocated=strategy_in.budget_allocated,
        regions_affected=strategy_in.regions_affected
    )
    return strategy


@router.put("/{strategy_id}", response_model=Strategy)
def update_strategy(
    strategy_id: UUID,
    strategy_in: StrategyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update strategy (owner or admin)
    """
    strategy = crud_strategy.get(db, strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Check permissions
    if current_user.role == UserRole.STRATEGY_OWNER and strategy.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this strategy"
        )
    
    update_data = strategy_in.dict(exclude_unset=True)
    strategy = crud_strategy.update(db, strategy_id, **update_data)
    return strategy


@router.delete("/{strategy_id}", response_model=Message, dependencies=[Depends(require_admin)])
def delete_strategy(
    strategy_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete strategy (admin only)
    """
    success = crud_strategy.delete(db, strategy_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    return Message(message="Strategy deleted successfully")


@router.get("/ministry/{ministry_id}", response_model=List[Strategy])
def get_ministry_strategies(
    ministry_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get all strategies for a ministry (public endpoint)
    """
    strategies = crud_strategy.get_by_ministry(db, ministry_id)
    return strategies


@router.get("/owner/me", response_model=List[Strategy])
def get_my_strategies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all strategies owned by current user
    """
    strategies = crud_strategy.get_by_owner(db, current_user.id)
    return strategies

