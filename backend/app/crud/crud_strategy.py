"""
CRUD operations for Strategy model
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
import uuid

from app.models.strategy import Strategy, StrategyStatus, StrategySector, NDPPillar


class CRUDStrategy:
    """CRUD operations for Strategy"""
    
    def get(self, db: Session, strategy_id: uuid.UUID) -> Optional[Strategy]:
        """Get strategy by ID"""
        return db.query(Strategy).filter(Strategy.id == strategy_id).first()
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        ministry_id: Optional[uuid.UUID] = None,
        status: Optional[StrategyStatus] = None,
        sector: Optional[StrategySector] = None
    ) -> List[Strategy]:
        """Get multiple strategies with filters"""
        query = db.query(Strategy)
        
        if ministry_id:
            query = query.filter(Strategy.ministry_id == ministry_id)
        if status:
            query = query.filter(Strategy.status == status)
        if sector:
            query = query.filter(Strategy.sector == sector)
        
        return query.order_by(Strategy.created_at.desc()).offset(skip).limit(limit).all()
    
    def search(self, db: Session, search_term: str, skip: int = 0, limit: int = 100) -> List[Strategy]:
        """Search strategies by title or description"""
        return db.query(Strategy).filter(
            or_(
                Strategy.title.ilike(f"%{search_term}%"),
                Strategy.description.ilike(f"%{search_term}%")
            )
        ).offset(skip).limit(limit).all()
    
    def get_by_ministry(self, db: Session, ministry_id: uuid.UUID) -> List[Strategy]:
        """Get all strategies for a ministry"""
        return db.query(Strategy).filter(Strategy.ministry_id == ministry_id).all()
    
    def get_by_owner(self, db: Session, owner_id: uuid.UUID) -> List[Strategy]:
        """Get all strategies owned by a user"""
        return db.query(Strategy).filter(Strategy.owner_id == owner_id).all()
    
    def create(
        self,
        db: Session,
        title: str,
        description: str,
        ministry_id: uuid.UUID,
        owner_id: uuid.UUID,
        announcement_date: datetime,
        start_date: datetime,
        end_date: datetime,
        sector: StrategySector,
        ndp_pillar: NDPPillar,
        document_url: Optional[str] = None,
        budget_allocated: Optional[float] = None,
        regions_affected: Optional[List[str]] = None
    ) -> Strategy:
        """Create new strategy"""
        strategy = Strategy(
            id=uuid.uuid4(),
            title=title,
            description=description,
            ministry_id=ministry_id,
            owner_id=owner_id,
            document_url=document_url,
            announcement_date=announcement_date,
            start_date=start_date,
            end_date=end_date,
            budget_allocated=budget_allocated,
            sector=sector,
            regions_affected=regions_affected or [],
            ndp_pillar=ndp_pillar,
            status=StrategyStatus.ACTIVE,
            visibility="PUBLIC"
        )
        db.add(strategy)
        db.commit()
        db.refresh(strategy)
        return strategy
    
    def update(
        self, 
        db: Session, 
        strategy_id: uuid.UUID, 
        **kwargs
    ) -> Optional[Strategy]:
        """Update strategy"""
        strategy = self.get(db, strategy_id)
        if not strategy:
            return None
        
        for key, value in kwargs.items():
            if hasattr(strategy, key):
                setattr(strategy, key, value)
        
        db.commit()
        db.refresh(strategy)
        return strategy
    
    def delete(self, db: Session, strategy_id: uuid.UUID) -> bool:
        """Delete strategy"""
        strategy = self.get(db, strategy_id)
        if not strategy:
            return False
        db.delete(strategy)
        db.commit()
        return True
    
    def get_active_count(self, db: Session) -> int:
        """Get count of active strategies"""
        return db.query(Strategy).filter(Strategy.status == StrategyStatus.ACTIVE).count()
    
    def get_statistics(self, db: Session) -> dict:
        """Get strategy statistics"""
        total = db.query(Strategy).count()
        active = db.query(Strategy).filter(Strategy.status == StrategyStatus.ACTIVE).count()
        completed = db.query(Strategy).filter(Strategy.status == StrategyStatus.COMPLETED).count()
        suspended = db.query(Strategy).filter(Strategy.status == StrategyStatus.SUSPENDED).count()
        
        return {
            "total": total,
            "active": active,
            "completed": completed,
            "suspended": suspended
        }


crud_strategy = CRUDStrategy()
