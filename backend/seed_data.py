"""Seed the database with sample data"""
import sys
import os
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.db.session import SessionLocal
from app.models.ministry import Ministry
from app.models.user import User
from app.models.strategy import Strategy
from datetime import datetime
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def seed_data():
    db = SessionLocal()
    
    try:
        # Check if we already have data
        if db.query(Ministry).count() > 0:
            print('Data already exists. Skipping seed.')
            return
        
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
        
        print(f'✓ Created {len(ministries)} ministries')
        
        # Create a sample admin user
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
        
        print('✓ Created admin user: admin@gov.na / Admin@2025')
        
        # Create sample strategies
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
        
        print(f'✓ Created {len(strategies)} strategies')
        print('\n✅ Sample data created successfully!')
        print('\nYou can now:')
        print('  - View strategies at http://localhost:3000')
        print('  - Login as admin@gov.na with password: Admin@2025')
        
    except Exception as e:
        print(f'❌ Error: {e}')
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == '__main__':
    seed_data()
