"""
Seed database with sample data for testing and demo
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime, timedelta
from app.db.session import SessionLocal
from app.models.ministry import Ministry
from app.models.user import User
from app.models.strategy import Strategy  
from app.models.milestone import Milestone
from app.models.question import Question, Response
from app.models.audit_log import AuditLog
from app.crud.crud_user import crud_user
from app.crud.crud_ministry import crud_ministry
from app.crud.crud_strategy import crud_strategy
from app.crud.crud_milestone import crud_milestone
from app.crud.crud_question import crud_question, crud_response
from app.models.user import UserRole
from app.models.strategy import StrategyStatus, StrategySector, NDPPillar
from app.models.milestone import MilestoneStatus
from app.core.security import get_password_hash


def seed_database():
    """Seed database with sample data"""
    db = SessionLocal()
    
    try:
        print("🌱 Starting database seeding...")
        
        # Check if data already exists
        existing_ministries = db.query(Ministry).count()
        if existing_ministries > 0:
            print(f"\n⚠️  Database already contains data ({existing_ministries} ministries)")
            response = input("Do you want to clear and reseed? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Seeding cancelled")
                return
            
            # Clear existing data
            print("\n🗑️  Clearing existing data...")
            
            db.query(Response).delete()
            db.query(Question).delete()
            db.query(Milestone).delete()
            db.query(Strategy).delete()
            db.query(User).delete()
            db.query(Ministry).delete()
            db.query(AuditLog).delete()
            db.commit()
            print("  ✓ Cleared existing data")
        
        # 1. Create Ministries
        print("\n📊 Creating ministries...")
        ministries = [
            {"name": "Ministry of Information and Communication Technology", "abbreviation": "MICT", "website": "https://mict.gov.na"},
            {"name": "Ministry of Mines and Energy", "abbreviation": "MME", "website": "https://mme.gov.na"},
            {"name": "Ministry of Agriculture, Water and Land Reform", "abbreviation": "MAWLR", "website": "https://mawlr.gov.na"},
            {"name": "Ministry of Health and Social Services", "abbreviation": "MHSS", "website": "https://mhss.gov.na"},
            {"name": "Ministry of Education, Arts and Culture", "abbreviation": "MEAC", "website": "https://meac.gov.na"},
        ]
        
        ministry_objects = []
        for m in ministries:
            ministry = crud_ministry.create(db, name=m["name"], abbreviation=m["abbreviation"], website=m["website"])
            ministry_objects.append(ministry)
            print(f"  ✓ Created {m['abbreviation']}")
        
        # 2. Create Users
        print("\n👥 Creating users...")
        
        # Platform Admin
        admin_user = crud_user.create(
            db,
            email="admin@govt.na",
            password="Admin123!@#",
            first_name="Platform",
            last_name="Administrator",
            role=UserRole.PLATFORM_ADMIN,
            ministry_id=None
        )
        print(f"  ✓ Created Platform Admin: admin@govt.na")
        
        # Ministry Admins and Strategy Owners
        users = []
        for i, ministry in enumerate(ministry_objects):
            # Ministry Admin
            admin = crud_user.create(
                db,
                email=f"admin.{ministry.abbreviation.lower()}@govt.na",
                password="Admin123!@#",
                first_name=f"{ministry.abbreviation}",
                last_name="Administrator",
                role=UserRole.MINISTRY_ADMIN,
                ministry_id=ministry.id
            )
            users.append(admin)
            print(f"  ✓ Created Ministry Admin: {admin.email}")
            
            # Strategy Owner
            owner = crud_user.create(
                db,
                email=f"owner.{ministry.abbreviation.lower()}@govt.na",
                password="Owner123!@#",
                first_name=f"{ministry.abbreviation}",
                last_name="Strategy Owner",
                role=UserRole.STRATEGY_OWNER,
                ministry_id=ministry.id
            )
            users.append(owner)
            print(f"  ✓ Created Strategy Owner: {owner.email}")
        
        # 3. Create Strategies
        print("\n📋 Creating strategies...")
        
        strategies_data = [
            {
                "title": "National Green Hydrogen Strategy",
                "description": "Develop Namibia into a leading green hydrogen producer and exporter by 2030, leveraging renewable energy resources to create sustainable economic growth.",
                "ministry_idx": 1,  # MME
                "sector": StrategySector.ENERGY,
                "ndp_pillar": NDPPillar.ECONOMIC_PROGRESSION,
                "budget": 2500000000,
                "regions": ["Erongo", "Kunene", "Hardap"]
            },
            {
                "title": "Digital Transformation Strategy",
                "description": "Accelerate digital transformation across government services, improve connectivity, and enhance ICT infrastructure nationwide.",
                "ministry_idx": 0,  # MICT
                "sector": StrategySector.TECHNOLOGY,
                "ndp_pillar": NDPPillar.INFRASTRUCTURE_DEVELOPMENT,
                "budget": 500000000,
                "regions": ["All Regions"]
            },
            {
                "title": "Food Security and Agricultural Development Plan",
                "description": "Ensure food security through sustainable agricultural practices, irrigation development, and support for small-scale farmers.",
                "ministry_idx": 2,  # MAWLR
                "sector": StrategySector.AGRICULTURE,
                "ndp_pillar": NDPPillar.ECONOMIC_PROGRESSION,
                "budget": 800000000,
                "regions": ["Kavango East", "Kavango West", "Zambezi", "Ohangwena"]
            },
            {
                "title": "Universal Health Coverage Roadmap",
                "description": "Achieve universal health coverage by 2030, improving healthcare infrastructure and service delivery across all regions.",
                "ministry_idx": 3,  # MHSS
                "sector": StrategySector.HEALTH,
                "ndp_pillar": NDPPillar.SOCIAL_PROGRESSION,
                "budget": 1200000000,
                "regions": ["All Regions"]
            },
            {
                "title": "Education Quality Enhancement Program",
                "description": "Improve education quality through teacher training, curriculum reform, and infrastructure development in schools.",
                "ministry_idx": 4,  # MEAC
                "sector": StrategySector.EDUCATION,
                "ndp_pillar": NDPPillar.SOCIAL_PROGRESSION,
                "budget": 650000000,
                "regions": ["All Regions"]
            }
        ]
        
        strategy_objects = []
        for idx, s_data in enumerate(strategies_data):
            ministry = ministry_objects[s_data["ministry_idx"]]
            owner = users[s_data["ministry_idx"] * 2 + 1]  # Strategy owner for ministry
            
            strategy = crud_strategy.create(
                db,
                title=s_data["title"],
                description=s_data["description"],
                ministry_id=ministry.id,
                owner_id=owner.id,
                announcement_date=datetime.utcnow() - timedelta(days=180),
                start_date=datetime.utcnow() - timedelta(days=150),
                end_date=datetime.utcnow() + timedelta(days=1600),
                sector=s_data["sector"],
                ndp_pillar=s_data["ndp_pillar"],
                budget_allocated=s_data["budget"],
                regions_affected=s_data["regions"]
            )
            strategy_objects.append(strategy)
            print(f"  ✓ Created strategy: {s_data['title'][:50]}...")
        
        # 4. Create Milestones
        print("\n🎯 Creating milestones...")
        
        # Milestones for Green Hydrogen Strategy
        green_hydrogen_milestones = [
            {"title": "Feasibility Study Completion", "description": "Complete comprehensive feasibility study", "months": -2, "status": MilestoneStatus.COMPLETED, "completion": 100},
            {"title": "Investor Engagement", "description": "Secure commitments from international investors", "months": 3, "status": MilestoneStatus.IN_PROGRESS, "completion": 75},
            {"title": "Regulatory Framework", "description": "Establish legal and regulatory framework", "months": 6, "status": MilestoneStatus.IN_PROGRESS, "completion": 50},
            {"title": "Infrastructure Development", "description": "Begin construction of production facilities", "months": 12, "status": MilestoneStatus.NOT_STARTED, "completion": 0},
            {"title": "First Production", "description": "Commence initial hydrogen production", "months": 36, "status": MilestoneStatus.NOT_STARTED, "completion": 0},
        ]
        
        for order, m_data in enumerate(green_hydrogen_milestones):
            milestone = crud_milestone.create(
                db,
                strategy_id=strategy_objects[0].id,
                title=m_data["title"],
                description=m_data["description"],
                target_date=datetime.utcnow() + timedelta(days=m_data["months"]*30),
                responsible_officer=users[3].email,  # MME Strategy Owner
                order_index=order,
                kpi=f"{m_data['completion']}% completion target"
            )
            # Update status and progress
            crud_milestone.update_progress(db, milestone.id, m_data["status"], m_data["completion"])
            print(f"    ✓ Created milestone: {m_data['title']}")
        
        # Milestones for Digital Transformation
        digital_milestones = [
            {"title": "Infrastructure Assessment", "description": "Assess current ICT infrastructure", "months": -1, "status": MilestoneStatus.COMPLETED, "completion": 100},
            {"title": "E-Government Portal Development", "description": "Develop centralized e-government services portal", "months": 4, "status": MilestoneStatus.IN_PROGRESS, "completion": 60},
            {"title": "Connectivity Expansion", "description": "Expand broadband connectivity to rural areas", "months": 8, "status": MilestoneStatus.NOT_STARTED, "completion": 15},
            {"title": "Digital Skills Training", "description": "Train 10,000 citizens in digital literacy", "months": 12, "status": MilestoneStatus.NOT_STARTED, "completion": 0},
        ]
        
        for order, m_data in enumerate(digital_milestones):
            milestone = crud_milestone.create(
                db,
                strategy_id=strategy_objects[1].id,
                title=m_data["title"],
                description=m_data["description"],
                target_date=datetime.utcnow() + timedelta(days=m_data["months"]*30),
                responsible_officer=users[1].email,  # MICT Strategy Owner
                order_index=order
            )
            crud_milestone.update_progress(db, milestone.id, m_data["status"], m_data["completion"])
            print(f"    ✓ Created milestone: {m_data['title']}")
        
        # 5. Create Questions
        print("\n❓ Creating questions...")
        
        questions_data = [
            {
                "strategy_idx": 0,
                "text": "What is the expected timeline for the first green hydrogen production?",
                "submitter": "John Namibia",
                "email": "john@example.com",
                "approved": True,
                "answer": "Initial production is targeted for Q2 2028. We are currently finalizing investor agreements and regulatory frameworks, which will pave the way for infrastructure development beginning in 2026."
            },
            {
                "strategy_idx": 0,
                "text": "How many jobs will this project create for Namibians?",
                "submitter": "Maria Santos",
                "email": "maria@example.com",
                "approved": True,
                "answer": "The Green Hydrogen project is expected to create approximately 15,000 direct jobs during construction phase and 3,000 permanent jobs during operations. We are committed to ensuring Namibians benefit through skills development programs."
            },
            {
                "strategy_idx": 1,
                "text": "When will the e-government portal be available to citizens?",
                "submitter": "Peter Smith",
                "email": None,
                "approved": True,
                "answer": "The e-government portal is scheduled to launch in Q3 2025. It will initially offer 15 key services including passport applications, business registration, and tax filing. More services will be added progressively."
            },
            {
                "strategy_idx": 1,
                "text": "How will you ensure rural areas are not left behind in digital transformation?",
                "submitter": None,
                "email": None,
                "approved": True,
                "answer": None  # Unanswered
            },
            {
                "strategy_idx": 2,
                "text": "What support will be provided to small-scale farmers?",
                "submitter": "Anna Farmer",
                "email": "anna@example.com",
                "approved": False,  # Pending moderation
                "answer": None
            },
        ]
        
        for q_data in questions_data:
            question = crud_question.create(
                db,
                strategy_id=strategy_objects[q_data["strategy_idx"]].id,
                question_text=q_data["text"],
                submitter_name=q_data["submitter"],
                submitter_email=q_data["email"]
            )
            
            if q_data["approved"]:
                # Approve question
                crud_question.moderate(db, question.id, admin_user.id, True, "Approved")
                print(f"  ✓ Created and approved question: {q_data['text'][:60]}...")
                
                # Add answer if provided
                if q_data["answer"]:
                    owner_idx = strategies_data[q_data["strategy_idx"]]["ministry_idx"] * 2 + 1
                    response = crud_response.create(
                        db,
                        question_id=question.id,
                        user_id=users[owner_idx].id,
                        response_text=q_data["answer"]
                    )
                    print(f"    ✓ Added response")
            else:
                print(f"  ✓ Created pending question: {q_data['text'][:60]}...")
        
        print("\n✅ Database seeding completed successfully!")
        print("\n📝 Summary:")
        print(f"  - Ministries: {len(ministry_objects)}")
        print(f"  - Users: {len(users) + 1} (1 platform admin, {len(ministry_objects)} ministry admins, {len(ministry_objects)} strategy owners)")
        print(f"  - Strategies: {len(strategy_objects)}")
        print(f"  - Milestones: {len(green_hydrogen_milestones) + len(digital_milestones)}")
        print(f"  - Questions: {len(questions_data)}")
        
        print("\n🔐 Login Credentials:")
        print("\nPlatform Admin:")
        print("  Email: admin@govt.na")
        print("  Password: Admin123!@#")
        
        print("\nMinistry Admins:")
        for ministry in ministry_objects:
            print(f"  {ministry.abbreviation}: admin.{ministry.abbreviation.lower()}@govt.na / Admin123!@#")
        
        print("\nStrategy Owners:")
        for ministry in ministry_objects:
            print(f"  {ministry.abbreviation}: owner.{ministry.abbreviation.lower()}@govt.na / Owner123!@#")
        
        print("\n🌐 API Endpoints to test:")
        print("  - GET http://localhost:8000/api/v1/ministries/")
        print("  - GET http://localhost:8000/api/v1/strategies/")
        print("  - GET http://localhost:8000/api/v1/strategies/stats")
        print("  - POST http://localhost:8000/api/v1/auth/login")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
