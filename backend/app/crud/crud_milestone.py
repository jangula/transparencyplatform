"""
CRUD operations for Milestone model
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.models.milestone import Milestone, MilestoneStatus


class CRUDMilestone:
    """CRUD operations for Milestone"""
    
    def get(self, db: Session, milestone_id: uuid.UUID) -> Optional[Milestone]:
        """Get milestone by ID"""
        return db.query(Milestone).filter(Milestone.id == milestone_id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        strategy_id: Optional[uuid.UUID] = None,
        status: Optional[MilestoneStatus] = None
    ) -> List[Milestone]:
        """Get multiple milestones with filters"""
        query = db.query(Milestone)
        
        if strategy_id:
            query = query.filter(Milestone.strategy_id == strategy_id)
        if status:
            query = query.filter(Milestone.status == status)
        
        return query.order_by(Milestone.order_index).offset(skip).limit(limit).all()
    
    def get_by_strategy(self, db: Session, strategy_id: uuid.UUID) -> List[Milestone]:
        """Get all milestones for a strategy"""
        return db.query(Milestone).filter(
            Milestone.strategy_id == strategy_id
        ).order_by(Milestone.order_index).all()
    
    def create(
        self,
        db: Session,
        strategy_id: uuid.UUID,
        title: str,
        description: str,
        target_date: datetime,
        responsible_officer: str,
        order_index: int,
        kpi: Optional[str] = None
    ) -> Milestone:
        """Create new milestone"""
        milestone = Milestone(
            id=uuid.uuid4(),
            strategy_id=strategy_id,
            title=title,
            description=description,
            target_date=target_date,
            responsible_officer=responsible_officer,
            kpi=kpi,
            status=MilestoneStatus.NOT_STARTED,
            completion_percentage=0,
            order_index=order_index
        )
        db.add(milestone)
        db.commit()
        db.refresh(milestone)
        return milestone
    
    def update(
        self, 
        db: Session, 
        milestone_id: uuid.UUID, 
        **kwargs
    ) -> Optional[Milestone]:
        """Update milestone"""
        milestone = self.get(db, milestone_id)
        if not milestone:
            return None
        
        for key, value in kwargs.items():
            if hasattr(milestone, key):
                setattr(milestone, key, value)
        
        db.commit()
        db.refresh(milestone)
        return milestone
    
    def delete(self, db: Session, milestone_id: uuid.UUID) -> bool:
        """Delete milestone"""
        milestone = self.get(db, milestone_id)
        if not milestone:
            return False
        db.delete(milestone)
        db.commit()
        return True
    
    def update_progress(
        self,
        db: Session,
        milestone_id: uuid.UUID,
        status: MilestoneStatus,
        completion_percentage: int
    ) -> Optional[Milestone]:
        """Update milestone progress"""
        milestone = self.get(db, milestone_id)
        if not milestone:
            return None
        
        milestone.status = status
        milestone.completion_percentage = completion_percentage
        db.commit()
        db.refresh(milestone)
        return milestone
    
    def get_completed_count(self, db: Session, strategy_id: uuid.UUID) -> int:
        """Get count of completed milestones for a strategy"""
        return db.query(Milestone).filter(
            Milestone.strategy_id == strategy_id,
            Milestone.status == MilestoneStatus.COMPLETED
        ).count()
    
    def get_overdue(self, db: Session) -> List[Milestone]:
        """Get all overdue milestones"""
        return db.query(Milestone).filter(
            Milestone.status != MilestoneStatus.COMPLETED,
            Milestone.target_date < datetime.utcnow()
        ).all()


crud_milestone = CRUDMilestone()
