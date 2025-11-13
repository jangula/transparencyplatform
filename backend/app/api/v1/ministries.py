"""
Ministry API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.deps import get_db, get_current_user, require_admin
from app.crud.crud_ministry import crud_ministry
from app.schemas.ministry import Ministry, MinistryCreate, MinistryUpdate, MinistryList
from app.schemas.common import Message
from app.models.user import User

router = APIRouter()


@router.get("/", response_model=MinistryList)
def list_ministries(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of all ministries (public endpoint)
    """
    ministries = crud_ministry.get_multi(db, skip=skip, limit=limit)
    total = crud_ministry.count(db)
    return MinistryList(ministries=ministries, total=total)


@router.get("/{ministry_id}", response_model=Ministry)
def get_ministry(
    ministry_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get ministry by ID (public endpoint)
    """
    ministry = crud_ministry.get(db, ministry_id)
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    return ministry


@router.post("/", response_model=Ministry, dependencies=[Depends(require_admin)])
def create_ministry(
    ministry_in: MinistryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create new ministry (admin only)
    """
    # Check if ministry with same name exists
    existing = crud_ministry.get_by_name(db, ministry_in.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ministry with this name already exists"
        )
    
    # Check abbreviation
    existing_abbr = crud_ministry.get_by_abbreviation(db, ministry_in.abbreviation)
    if existing_abbr:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ministry with this abbreviation already exists"
        )
    
    ministry = crud_ministry.create(
        db,
        name=ministry_in.name,
        abbreviation=ministry_in.abbreviation,
        website=str(ministry_in.website) if ministry_in.website else None
    )
    return ministry


@router.put("/{ministry_id}", response_model=Ministry, dependencies=[Depends(require_admin)])
def update_ministry(
    ministry_id: UUID,
    ministry_in: MinistryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update ministry (admin only)
    """
    ministry = crud_ministry.get(db, ministry_id)
    if not ministry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    
    update_data = ministry_in.dict(exclude_unset=True)
    if 'website' in update_data and update_data['website']:
        update_data['website'] = str(update_data['website'])
    
    ministry = crud_ministry.update(db, ministry_id, **update_data)
    return ministry


@router.delete("/{ministry_id}", response_model=Message, dependencies=[Depends(require_admin)])
def delete_ministry(
    ministry_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete ministry (admin only)
    """
    success = crud_ministry.delete(db, ministry_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ministry not found"
        )
    return Message(message="Ministry deleted successfully")

