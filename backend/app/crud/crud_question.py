"""
CRUD operations for Question and Response models
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.question import Question, Response, QuestionStatus


class CRUDQuestion:
    """CRUD operations for Question"""
    
    def get(self, db: Session, question_id: uuid.UUID) -> Optional[Question]:
        """Get question by ID"""
        return db.query(Question).filter(Question.id == question_id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        strategy_id: Optional[uuid.UUID] = None,
        status: Optional[QuestionStatus] = None
    ) -> List[Question]:
        """Get multiple questions with filters"""
        query = db.query(Question)
        
        if strategy_id:
            query = query.filter(Question.strategy_id == strategy_id)
        if status:
            query = query.filter(Question.status == status)
        
        return query.order_by(Question.submitted_at.desc()).offset(skip).limit(limit).all()
    
    def get_by_strategy(
        self,
        db: Session,
        strategy_id: uuid.UUID,
        status: QuestionStatus = QuestionStatus.PUBLISHED,
        skip: int = 0,
        limit: int = 100
    ) -> List[Question]:
        """Get all questions for a strategy with optional status filter"""
        query = db.query(Question).filter(Question.strategy_id == strategy_id)
        
        if status:
            query = query.filter(Question.status == status)
        
        return query.order_by(Question.submitted_at.desc()).offset(skip).limit(limit).all()
    
    def get_pending(self, db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get pending questions for moderation"""
        return db.query(Question).filter(
            Question.status == QuestionStatus.PENDING_MODERATION
        ).order_by(Question.submitted_at).offset(skip).limit(limit).all()
    
    def create(
        self,
        db: Session,
        strategy_id: uuid.UUID,
        question_text: str,
        submitter_name: Optional[str] = None,
        submitter_email: Optional[str] = None
    ) -> Question:
        """Create new question"""
        question = Question(
            id=uuid.uuid4(),
            strategy_id=strategy_id,
            submitter_name=submitter_name,
            submitter_email=submitter_email,
            question_text=question_text,
            status=QuestionStatus.PENDING_MODERATION,
            submitted_at=datetime.utcnow()
        )
        db.add(question)
        db.commit()
        db.refresh(question)
        return question
    
    def moderate(
        self,
        db: Session,
        question_id: uuid.UUID,
        moderator_id: uuid.UUID,
        approved: bool,
        moderation_notes: Optional[str] = None
    ) -> Optional[Question]:
        """Moderate a question"""
        question = self.get(db, question_id)
        if not question:
            return None
        
        question.status = QuestionStatus.PUBLISHED if approved else QuestionStatus.REJECTED
        question.moderated_by = moderator_id
        question.moderated_at = datetime.utcnow()
        question.moderation_notes = moderation_notes
        
        db.commit()
        db.refresh(question)
        return question
    
    def delete(self, db: Session, question_id: uuid.UUID) -> bool:
        """Delete question"""
        question = self.get(db, question_id)
        if not question:
            return False
        db.delete(question)
        db.commit()
        return True
    
    def count_pending(self, db: Session) -> int:
        """Count pending questions"""
        return db.query(Question).filter(
            Question.status == QuestionStatus.PENDING_MODERATION
        ).count()
    
    def count_unanswered(self, db: Session) -> int:
        """Count published but unanswered questions"""
        # Questions with no response
        return db.query(Question).outerjoin(Response).filter(
            Question.status == QuestionStatus.PUBLISHED,
            Response.id == None
        ).count()
    
    def get_published(self, db: Session, skip: int = 0, limit: int = 100) -> List[Question]:
        """Get all published questions"""
        return db.query(Question).filter(
            Question.status == QuestionStatus.PUBLISHED
        ).order_by(Question.submitted_at.desc()).offset(skip).limit(limit).all()
    
    def count_published(self, db: Session) -> int:
        """Count all published questions"""
        return db.query(Question).filter(
            Question.status == QuestionStatus.PUBLISHED
        ).count()
    
    def count_by_strategy(self, db: Session, strategy_id: uuid.UUID) -> int:
        """Count all published questions for a strategy"""
        return db.query(Question).filter(
            Question.strategy_id == strategy_id,
            Question.status == QuestionStatus.PUBLISHED
        ).count()
    
    def count_answered_by_strategy(self, db: Session, strategy_id: uuid.UUID) -> int:
        """Count answered questions for a strategy"""
        return db.query(Question).join(Response).filter(
            Question.strategy_id == strategy_id,
            Question.status == QuestionStatus.PUBLISHED
        ).count()
    
    def count_unanswered_by_strategy(self, db: Session, strategy_id: uuid.UUID) -> int:
        """Count unanswered questions for a strategy"""
        return db.query(Question).outerjoin(Response).filter(
            Question.strategy_id == strategy_id,
            Question.status == QuestionStatus.PUBLISHED,
            Response.id == None
        ).count()
    
    def approve(
        self,
        db: Session,
        question_id: uuid.UUID,
        moderator_id: uuid.UUID,
        notes: Optional[str] = None
    ) -> Optional[Question]:
        """Approve a question"""
        question = self.get(db, question_id)
        if not question:
            return None
        
        question.status = QuestionStatus.PUBLISHED
        question.moderated_by = moderator_id
        question.moderated_at = datetime.utcnow()
        question.moderation_notes = notes
        
        db.commit()
        db.refresh(question)
        return question
    
    def reject(
        self,
        db: Session,
        question_id: uuid.UUID,
        moderator_id: uuid.UUID,
        notes: Optional[str] = None
    ) -> Optional[Question]:
        """Reject a question"""
        question = self.get(db, question_id)
        if not question:
            return None
        
        question.status = QuestionStatus.REJECTED
        question.moderated_by = moderator_id
        question.moderated_at = datetime.utcnow()
        question.moderation_notes = notes
        
        db.commit()
        db.refresh(question)
        return question
    
    def create_response(
        self,
        db: Session,
        question_id: uuid.UUID,
        user_id: uuid.UUID,
        response_text: str
    ) -> Response:
        """Create a response to a question"""
        response = Response(
            id=uuid.uuid4(),
            question_id=question_id,
            user_id=user_id,
            response_text=response_text,
            published_at=datetime.utcnow()
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        return response


class CRUDResponse:
    """CRUD operations for Response"""
    
    def get(self, db: Session, response_id: uuid.UUID) -> Optional[Response]:
        """Get response by ID"""
        return db.query(Response).filter(Response.id == response_id).first()
    
    def get_by_question(self, db: Session, question_id: uuid.UUID) -> Optional[Response]:
        """Get response for a question"""
        return db.query(Response).filter(Response.question_id == question_id).first()
    
    def create(
        self,
        db: Session,
        question_id: uuid.UUID,
        user_id: uuid.UUID,
        response_text: str
    ) -> Response:
        """Create new response"""
        response = Response(
            id=uuid.uuid4(),
            question_id=question_id,
            user_id=user_id,
            response_text=response_text,
            published_at=datetime.utcnow()
        )
        db.add(response)
        db.commit()
        db.refresh(response)
        return response
    
    def update(
        self,
        db: Session,
        response_id: uuid.UUID,
        response_text: str
    ) -> Optional[Response]:
        """Update response"""
        response = self.get(db, response_id)
        if not response:
            return None
        
        response.response_text = response_text
        db.commit()
        db.refresh(response)
        return response
    
    def delete(self, db: Session, response_id: uuid.UUID) -> bool:
        """Delete response"""
        response = self.get(db, response_id)
        if not response:
            return False
        db.delete(response)
        db.commit()
        return True


crud_question = CRUDQuestion()
crud_response = CRUDResponse()
