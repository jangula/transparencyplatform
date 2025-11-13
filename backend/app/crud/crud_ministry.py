"""
CRUD operations for Ministry model
"""
from typing import Optional, List
from sqlalchemy.orm import Session
import uuid

from app.models.ministry import Ministry


class CRUDMinistry:
    """CRUD operations for Ministry"""
    
    def get(self, db: Session, ministry_id: uuid.UUID) -> Optional[Ministry]:
        """Get ministry by ID"""
        return db.query(Ministry).filter(Ministry.id == ministry_id).first()
    
    def get_by_name(self, db: Session, name: str) -> Optional[Ministry]:
        """Get ministry by name"""
        return db.query(Ministry).filter(Ministry.name == name).first()
    
    def get_by_abbreviation(self, db: Session, abbreviation: str) -> Optional[Ministry]:
        """Get ministry by abbreviation"""
        return db.query(Ministry).filter(Ministry.abbreviation == abbreviation).first()
    
    def get_multi(self, db: Session, skip: int = 0, limit: int = 100) -> List[Ministry]:
        """Get multiple ministries with pagination"""
        return db.query(Ministry).offset(skip).limit(limit).all()
    
    def get_all(self, db: Session) -> List[Ministry]:
        """Get all ministries"""
        return db.query(Ministry).all()
    
    def create(
        self, 
        db: Session, 
        name: str, 
        abbreviation: str,
        website: Optional[str] = None
    ) -> Ministry:
        """Create new ministry"""
        ministry = Ministry(
            id=uuid.uuid4(),
            name=name,
            abbreviation=abbreviation,
            website=website
        )
        db.add(ministry)
        db.commit()
        db.refresh(ministry)
        return ministry
    
    def update(
        self, 
        db: Session, 
        ministry_id: uuid.UUID, 
        **kwargs
    ) -> Optional[Ministry]:
        """Update ministry"""
        ministry = self.get(db, ministry_id)
        if not ministry:
            return None
        
        for key, value in kwargs.items():
            if hasattr(ministry, key):
                setattr(ministry, key, value)
        
        db.commit()
        db.refresh(ministry)
        return ministry
    
    def delete(self, db: Session, ministry_id: uuid.UUID) -> bool:
        """Delete ministry"""
        ministry = self.get(db, ministry_id)
        if not ministry:
            return False
        db.delete(ministry)
        db.commit()
        return True
    
    def count(self, db: Session) -> int:
        """Count total ministries"""
        return db.query(Ministry).count()


crud_ministry = CRUDMinistry()
