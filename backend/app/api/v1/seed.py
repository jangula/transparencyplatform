"""
Seed endpoint for development
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.ministry import Ministry
from app.models.user import User
from app.models.strategy import Strategy
from datetime import datetime
import uuid
from passlib.context import CryptContext

router = APIRouter()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    """Seed the database with sample data (development only)"""
    
    # Check if data already exists
    if db.query(Ministry).count() > 0:
        return {"message": "Database already seeded"}
    
    # Create Ministries
    ministries = [
        Ministry(
            id=str(uuid.uuid4()),
            name='Ministry of Mines, Energy and Industry',
            abbreviation='MMEI',
            website='https://mmei.gov.na'
        ),
        Ministry(
            id=str(uuid.uuid4()),
            name='Ministry of Agriculture',
            abbreviation='MA',
            website='https://agriculture.gov.na'
        ),
        Ministry(
            id=str(uuid.uuid4()),
            name='Ministry of ICT',
            abbreviation='MICT',
            website='https://mict.gov.na'
        ),
    ]
    
    for ministry in ministries:
        db.add(ministry)
    db.commit()
    for m in ministries:
        db.refresh(m)
    
    # Create admin user
    admin = User(
        id=str(uuid.uuid4()),
        email='admin@gov.na',
        password_hash=pwd_context.hash('Admin@2025'),
        first_name='Admin',
        last_name='User',
        role='PLATFORM_ADMIN',
        ministry_id=ministries[0].id,
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    # Create strategies
    strategies = [
        Strategy(
            id=str(uuid.uuid4()),
            title='Green Hydrogen Strategy',
            description='Developing Namibia as a leading green hydrogen producer in Africa through strategic partnerships and infrastructure development.',
            ministry_id=ministries[0].id,
            owner_id=admin.id,
            document_url='https://example.com/green-hydrogen.pdf',
            announcement_date=datetime(2024, 1, 1),
            start_date=datetime(2024, 1, 1),
            end_date=datetime(2030, 12, 31),
            budget_allocated=2500000000,
            sector='ENERGY',
            regions_affected=['Erongo', 'Kunene'],
            status='ACTIVE'
        ),
        Strategy(
            id=str(uuid.uuid4()),
            title='National Food Security Plan',
            description='Ensuring food security for all Namibians through sustainable agriculture, improved irrigation systems, and farmer support programs.',
            ministry_id=ministries[1].id,
            owner_id=admin.id,
            document_url='https://example.com/food-security.pdf',
            announcement_date=datetime(2024, 2, 1),
            start_date=datetime(2024, 3, 1),
            end_date=datetime(2029, 12, 31),
            budget_allocated=1200000000,
            sector='AGRICULTURE',
            regions_affected=['All Regions'],
            status='ACTIVE'
        ),
        Strategy(
            id=str(uuid.uuid4()),
            title='Digital Transformation Strategy',
            description='Digitizing government services and improving ICT infrastructure nationwide to enhance service delivery and efficiency.',
            ministry_id=ministries[2].id,
            owner_id=admin.id,
            document_url='https://example.com/digital-transform.pdf',
            announcement_date=datetime(2024, 3, 1),
            start_date=datetime(2024, 4, 1),
            end_date=datetime(2028, 12, 31),
            budget_allocated=800000000,
            sector='ICT',
            regions_affected=['All Regions'],
            status='ACTIVE'
        ),
    ]
    
    for strategy in strategies:
        db.add(strategy)
    db.commit()
    
    return {
        "message": "Database seeded successfully",
        "ministries_created": len(ministries),
        "users_created": 1,
        "strategies_created": len(strategies),
        "login_credentials": {
            "email": "admin@gov.na",
            "password": "Admin@2025"
        }
    }
