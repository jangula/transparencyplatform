"""
API endpoints for questions and answers (Q&A)
Citizens can ask questions, admins moderate, strategy owners respond
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.deps import get_db, get_current_user, get_current_platform_admin
from app.models.user import User
from app.models.question import QuestionStatus
from app.schemas.question import (
    QuestionCreate,
    QuestionResponse,
    QuestionUpdate,
    QuestionList,
    ResponseCreate,
    ResponseResponse,
    QuestionWithResponse
)
from app.crud.crud_question import crud_question

router = APIRouter()


@router.post("/", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def submit_question(
    question_in: QuestionCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a new question (public endpoint)
    Questions must be moderated before being published
    """
    # Validate strategy exists
    from app.crud.crud_strategy import crud_strategy
    strategy = crud_strategy.get(db, strategy_id=question_in.strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    # Create question with PENDING_MODERATION status
    question = crud_question.create(
        db,
        strategy_id=question_in.strategy_id,
        question_text=question_in.question_text,
        submitter_name=question_in.submitter_name,
        submitter_email=question_in.submitter_email
    )
    
    return question


@router.get("/", response_model=QuestionList)
def list_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    strategy_id: Optional[UUID] = None,
    status: Optional[QuestionStatus] = None,
    db: Session = Depends(get_db)
):
    """
    List all published questions (public endpoint)
    Can filter by strategy_id or status
    """
    if strategy_id:
        questions = crud_question.get_by_strategy(
            db,
            strategy_id=strategy_id,
            status=QuestionStatus.PUBLISHED,
            skip=skip,
            limit=limit
        )
        total = crud_question.count_by_strategy(db, strategy_id=strategy_id)
    else:
        questions = crud_question.get_published(db, skip=skip, limit=limit)
        total = crud_question.count_published(db)
    
    return {
        "questions": questions,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "page_size": limit
    }


@router.get("/pending", response_model=QuestionList)
def list_pending_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_platform_admin)
):
    """
    List questions pending moderation (admin only)
    """
    questions = crud_question.get_pending(db, skip=skip, limit=limit)
    total = crud_question.count_pending(db)
    
    return {
        "questions": questions,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "page_size": limit
    }


@router.get("/{question_id}", response_model=QuestionWithResponse)
def get_question(
    question_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get a specific question with its response (if any)
    Public endpoint
    """
    question = crud_question.get(db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    # Only show published questions to public
    if question.status != QuestionStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found or not yet published"
        )
    
    return question


@router.post("/{question_id}/moderate", response_model=QuestionResponse)
def moderate_question(
    question_id: UUID,
    action: str = Query(..., regex="^(approve|reject)$"),
    moderation_notes: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_platform_admin)
):
    """
    Approve or reject a question (admin only)
    """
    question = crud_question.get(db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.status != QuestionStatus.PENDING_MODERATION:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Question is already {question.status.value}"
        )
    
    if action == "approve":
        updated_question = crud_question.approve(
            db,
            question_id=question_id,
            moderator_id=current_user.id,
            notes=moderation_notes
        )
    else:  # reject
        updated_question = crud_question.reject(
            db,
            question_id=question_id,
            moderator_id=current_user.id,
            notes=moderation_notes
        )
    
    return updated_question


@router.post("/{question_id}/respond", response_model=ResponseResponse)
def respond_to_question(
    question_id: UUID,
    response_in: ResponseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Respond to a question (strategy owner, ministry admin, or platform admin)
    """
    question = crud_question.get(db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    if question.status != QuestionStatus.PUBLISHED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Can only respond to published questions"
        )
    
    # Check if user has permission to respond
    # (Strategy owner, ministry admin of that strategy's ministry, or platform admin)
    from app.crud.crud_strategy import crud_strategy
    strategy = crud_strategy.get(db, strategy_id=question.strategy_id)
    
    if current_user.role == "PLATFORM_ADMIN":
        # Platform admins can respond to anything
        pass
    elif current_user.role == "MINISTRY_ADMIN":
        # Ministry admins can respond to their ministry's questions
        if str(strategy.ministry_id) != str(current_user.ministry_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only respond to questions for your ministry"
            )
    elif current_user.role == "STRATEGY_OWNER":
        # Strategy owners can respond to their own strategies
        if str(strategy.owner_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only respond to questions for your strategies"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    
    # Create response
    response = crud_question.create_response(
        db,
        question_id=question_id,
        user_id=current_user.id,
        response_text=response_in.response_text
    )
    
    return response


@router.get("/strategy/{strategy_id}", response_model=QuestionList)
def get_questions_by_strategy(
    strategy_id: UUID,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all published questions for a specific strategy (public endpoint)
    """
    # Validate strategy exists
    from app.crud.crud_strategy import crud_strategy
    strategy = crud_strategy.get(db, strategy_id=strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    questions = crud_question.get_by_strategy(
        db,
        strategy_id=strategy_id,
        status=QuestionStatus.PUBLISHED,
        skip=skip,
        limit=limit
    )
    total = crud_question.count_by_strategy(db, strategy_id=strategy_id)
    
    return {
        "questions": questions,
        "total": total,
        "page": (skip // limit) + 1 if limit > 0 else 1,
        "page_size": limit
    }


@router.get("/strategy/{strategy_id}/stats")
def get_question_stats(
    strategy_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get Q&A statistics for a strategy (public endpoint)
    """
    # Validate strategy exists
    from app.crud.crud_strategy import crud_strategy
    strategy = crud_strategy.get(db, strategy_id=strategy_id)
    if not strategy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Strategy not found"
        )
    
    total_questions = crud_question.count_by_strategy(db, strategy_id=strategy_id)
    answered_questions = crud_question.count_answered_by_strategy(db, strategy_id=strategy_id)
    unanswered_questions = crud_question.count_unanswered_by_strategy(db, strategy_id=strategy_id)
    
    return {
        "strategy_id": strategy_id,
        "total_questions": total_questions,
        "answered": answered_questions,
        "unanswered": unanswered_questions,
        "response_rate": (answered_questions / total_questions * 100) if total_questions > 0 else 0
    }


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_platform_admin)
):
    """
    Delete a question (admin only)
    Used for spam or inappropriate content
    """
    question = crud_question.get(db, question_id=question_id)
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    crud_question.delete(db, id=question_id)
    return None
