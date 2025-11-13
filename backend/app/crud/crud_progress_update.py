"""
CRUD operations for progress updates
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from datetime import datetime, timedelta
from uuid import UUID

from app.models.progress_update import ProgressUpdate, MilestoneUpdate
from app.models.strategy import StrategyStatus


class CRUDProgressUpdate:
    """CRUD operations for progress updates"""
    
    def get(
        self,
        db: Session,
        id: UUID
    ) -> Optional[ProgressUpdate]:
        """Get a progress update by ID"""
        return db.query(ProgressUpdate).filter(ProgressUpdate.id == id).first()
    
    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProgressUpdate]:
        """Get multiple progress updates with pagination"""
        return (
            db.query(ProgressUpdate)
            .order_by(desc(ProgressUpdate.published_date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create(
        self,
        db: Session,
        *,
        strategy_id: UUID,
        user_id: UUID,
        update_period: str,
        overall_status: StrategyStatus,
        completion_percentage: int,
        achievements: str,
        challenges: Optional[str] = None,
        mitigation_measures: Optional[str] = None,
        next_steps: Optional[str] = None,
        evidence_urls: List[str] = None
    ) -> ProgressUpdate:
        """Create a new progress update"""
        db_obj = ProgressUpdate(
            strategy_id=strategy_id,
            user_id=user_id,
            update_period=update_period,
            overall_status=overall_status,
            completion_percentage=completion_percentage,
            achievements=achievements,
            challenges=challenges,
            mitigation_measures=mitigation_measures,
            next_steps=next_steps,
            evidence_urls=evidence_urls or [],
            published_date=datetime.utcnow()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_strategy(
        self,
        db: Session,
        *,
        strategy_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProgressUpdate]:
        """Get all progress updates for a strategy"""
        return (
            db.query(ProgressUpdate)
            .filter(ProgressUpdate.strategy_id == strategy_id)
            .order_by(desc(ProgressUpdate.published_date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_latest_by_strategy(
        self,
        db: Session,
        *,
        strategy_id: UUID
    ) -> Optional[ProgressUpdate]:
        """Get the most recent progress update for a strategy"""
        return (
            db.query(ProgressUpdate)
            .filter(ProgressUpdate.strategy_id == strategy_id)
            .order_by(desc(ProgressUpdate.published_date))
            .first()
        )
    
    def get_by_user(
        self,
        db: Session,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProgressUpdate]:
        """Get all progress updates by a user"""
        return (
            db.query(ProgressUpdate)
            .filter(ProgressUpdate.user_id == user_id)
            .order_by(desc(ProgressUpdate.published_date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_status(
        self,
        db: Session,
        *,
        status: StrategyStatus,
        skip: int = 0,
        limit: int = 100
    ) -> List[ProgressUpdate]:
        """Get progress updates by status"""
        return (
            db.query(ProgressUpdate)
            .filter(ProgressUpdate.overall_status == status)
            .order_by(desc(ProgressUpdate.published_date))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_overdue_strategies(self, db: Session, days: int = 90) -> List[dict]:
        """
        Get strategies that haven't been updated in X days
        Returns list of dicts with strategy info and days since last update
        """
        from app.models.strategy import Strategy
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Subquery to get latest update date per strategy
        from sqlalchemy import func
        subq = (
            db.query(
                ProgressUpdate.strategy_id,
                func.max(ProgressUpdate.published_date).label('last_update')
            )
            .group_by(ProgressUpdate.strategy_id)
            .subquery()
        )
        
        # Get strategies with no updates or old updates
        overdue_strategies = (
            db.query(Strategy)
            .outerjoin(subq, Strategy.id == subq.c.strategy_id)
            .filter(
                (subq.c.last_update == None) | (subq.c.last_update < cutoff_date)
            )
            .all()
        )
        
        result = []
        for strategy in overdue_strategies:
            latest_update = self.get_latest_by_strategy(db, strategy_id=strategy.id)
            days_since_update = (
                (datetime.utcnow() - latest_update.published_date).days
                if latest_update
                else None
            )
            
            result.append({
                "strategy_id": strategy.id,
                "strategy_title": strategy.title,
                "ministry": strategy.ministry.name if strategy.ministry else None,
                "last_update_date": latest_update.published_date if latest_update else None,
                "days_since_update": days_since_update
            })
        
        return result
    
    def count(self, db: Session) -> int:
        """Count total progress updates"""
        return db.query(ProgressUpdate).count()


class CRUDMilestoneUpdate:
    """CRUD operations for milestone updates"""
    
    def create(
        self,
        db: Session,
        *,
        progress_update_id: UUID,
        milestone_id: UUID,
        status: StrategyStatus,
        completion_percentage: int,
        notes: Optional[str] = None
    ) -> MilestoneUpdate:
        """Create a milestone update"""
        db_obj = MilestoneUpdate(
            progress_update_id=progress_update_id,
            milestone_id=milestone_id,
            status=status,
            completion_percentage=completion_percentage,
            notes=notes
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_progress_update(
        self,
        db: Session,
        *,
        progress_update_id: UUID
    ) -> List[MilestoneUpdate]:
        """Get all milestone updates for a progress update"""
        return (
            db.query(MilestoneUpdate)
            .filter(MilestoneUpdate.progress_update_id == progress_update_id)
            .all()
        )
    
    def get_by_milestone(
        self,
        db: Session,
        *,
        milestone_id: UUID
    ) -> List[MilestoneUpdate]:
        """Get all updates for a specific milestone"""
        return (
            db.query(MilestoneUpdate)
            .filter(MilestoneUpdate.milestone_id == milestone_id)
            .order_by(desc(MilestoneUpdate.created_at))
            .all()
        )


# Create singleton instances
crud_progress_update = CRUDProgressUpdate()
crud_milestone_update = CRUDMilestoneUpdate()
