"""
Database seeding script
Populates the database with sample data for testing and demonstration
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.user import User, UserRole
from app.models.ministry import Ministry
from app.models.strategy import Strategy, StrategyStatus, StrategySector, NDPPillar
from app.models.milestone import Milestone, MilestoneStatus
from app.models.progress_update import ProgressUpdate, OverallStatus
from app.models.question import Question, QuestionStatus
from app.models.audit_log import AuditLog
from app.core.security import get_password_hash
from uuid import uuid4
import random


def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created")


def seed_ministries(db: Session):
    """Seed ministries"""
    print("\nSeeding ministries...")
    
    ministries_data = [
        {
            "name": "Ministry of Mines and Energy",
            "abbreviation": "MME",
            "website": "https://www.mme.gov.na"
        },
        {
            "name": "Ministry of Agriculture, Water and Land Reform",
            "abbreviation": "MAWLR",
            "website": "https://www.mawlr.gov.na"
        },
        {
            "name": "Ministry of Health and Social Services",
            "abbreviation": "MHSS",
            "website": "https://www.mhss.gov.na"
        },
        {
            "name": "Ministry of Education, Arts and Culture",
            "abbreviation": "MEAC",
            "website": "https://www.moe.gov.na"
        },
        {
            "name": "Ministry of Environment, Forestry and Tourism",
            "abbreviation": "MEFT",
            "website": "https://www.meft.gov.na"
        }
    ]
    
    ministries = []
    for data in ministries_data:
        ministry = Ministry(**data)
        db.add(ministry)
        ministries.append(ministry)
    
    db.commit()
    for ministry in ministries:
        db.refresh(ministry)
    print(f"✓ Created {len(ministries)} ministries")
    return ministries


def seed_users(db: Session, ministries: list):
    """Seed users"""
    print("\nSeeding users...")
    
    # Platform admin
    admin = User(
        email="admin@gov.na",
        password_hash=get_password_hash("Admin@123456"),
        first_name="System",
        last_name="Administrator",
        role=UserRole.PLATFORM_ADMIN,
        is_active=True,
        mfa_enabled=False
    )
    db.add(admin)
    
    users = [admin]
    
    # Ministry admins (one per ministry)
    admin_names = [
        ("John", "Mukwena"),
        ("Sarah", "Nghidinwa"),
        ("David", "Shapwa"),
        ("Maria", "Amakali"),
        ("Peter", "Hamunyela")
    ]
    
    for i, ministry in enumerate(ministries):
        user = User(
            email=f"admin.{ministry.abbreviation.lower()}@gov.na",
            password_hash=get_password_hash("Admin@123456"),
            first_name=admin_names[i][0],
            last_name=admin_names[i][1],
            role=UserRole.MINISTRY_ADMIN,
            ministry_id=ministry.id,
            is_active=True,
            mfa_enabled=False
        )
        db.add(user)
        users.append(user)
    
    # Strategy owners (two per ministry)
    owner_names = [
        ("James", "Shipanga"), ("Anna", "Kamati"),
        ("Michael", "Haindongo"), ("Grace", "Shikongo"),
        ("Thomas", "Sheya"), ("Elizabeth", "Nambahu"),
        ("Daniel", "Haufiku"), ("Martha", "Namutenya"),
        ("Joseph", "Kautwima"), ("Rebecca", "Ueitele")
    ]
    
    idx = 0
    for ministry in ministries:
        for j in range(2):
            user = User(
                email=f"owner{idx+1}.{ministry.abbreviation.lower()}@gov.na",
                password_hash=get_password_hash("Owner@123456"),
                first_name=owner_names[idx][0],
                last_name=owner_names[idx][1],
                role=UserRole.STRATEGY_OWNER,
                ministry_id=ministry.id,
                is_active=True,
                mfa_enabled=False
            )
            db.add(user)
            users.append(user)
            idx += 1
    
    db.commit()
    for user in users:
        db.refresh(user)
    print(f"✓ Created {len(users)} users")
    return users


def seed_strategies(db: Session, ministries: list, users: list):
    """Seed strategies"""
    print("\nSeeding strategies...")
    
    # Get strategy owners
    owners = [u for u in users if u.role == UserRole.STRATEGY_OWNER]
    
    strategies_data = [
        {
            "title": "Green Hydrogen Strategy",
            "description": "Development of Namibia's green hydrogen industry to drive economic growth and energy transition. This comprehensive strategy aims to position Namibia as a leading producer of green hydrogen in Africa.",
            "ministry": ministries[0],  # MME
            "sector": StrategySector.ENERGY,
            "ndp_pillar": NDPPillar.ECONOMIC_PROGRESSION,
            "announcement_date": date(2024, 3, 15),
            "start_date": date(2024, 4, 1),
            "end_date": date(2030, 12, 31),
            "budget_allocated": 2500000000,  # NAD 2.5 billion
            "regions_affected": ["Erongo", "Kunene", "Karas"]
        },
        {
            "title": "Food Security and Nutrition Plan",
            "description": "Comprehensive plan to ensure food security for all Namibians through improved agricultural productivity, value chain development, and nutrition programs.",
            "ministry": ministries[1],  # MAWLR
            "sector": StrategySector.AGRICULTURE,
            "ndp_pillar": NDPPillar.SOCIAL_TRANSFORMATION,
            "announcement_date": date(2024, 2, 1),
            "start_date": date(2024, 4, 1),
            "end_date": date(2029, 3, 31),
            "budget_allocated": 850000000,  # NAD 850 million
            "regions_affected": ["Kavango East", "Kavango West", "Zambezi", "Ohangwena"]
        },
        {
            "title": "Universal Health Coverage Initiative",
            "description": "Implementation of universal health coverage to ensure all Namibians have access to quality healthcare services without financial hardship.",
            "ministry": ministries[2],  # MHSS
            "sector": StrategySector.HEALTH,
            "ndp_pillar": NDPPillar.SOCIAL_TRANSFORMATION,
            "announcement_date": date(2024, 1, 15),
            "start_date": date(2024, 4, 1),
            "end_date": date(2028, 3, 31),
            "budget_allocated": 1200000000,  # NAD 1.2 billion
            "regions_affected": ["All regions"]
        },
        {
            "title": "Digital Education Transformation",
            "description": "Modernization of education system through digital technologies, improved infrastructure, and teacher training to prepare students for the 21st century.",
            "ministry": ministries[3],  # MEAC
            "sector": StrategySector.EDUCATION,
            "ndp_pillar": NDPPillar.ECONOMIC_PROGRESSION,
            "announcement_date": date(2024, 4, 10),
            "start_date": date(2024, 7, 1),
            "end_date": date(2029, 6, 30),
            "budget_allocated": 650000000,  # NAD 650 million
            "regions_affected": ["All regions"]
        },
        {
            "title": "Wildlife Conservation and Community Tourism",
            "description": "Sustainable wildlife conservation integrated with community-based tourism to create jobs and protect biodiversity.",
            "ministry": ministries[4],  # MEFT
            "sector": StrategySector.TOURISM,
            "ndp_pillar": NDPPillar.ENVIRONMENTAL_SUSTAINABILITY,
            "announcement_date": date(2024, 5, 20),
            "start_date": date(2024, 7, 1),
            "end_date": date(2030, 6, 30),
            "budget_allocated": 450000000,  # NAD 450 million
            "regions_affected": ["Kunene", "Zambezi", "Erongo", "Karas"]
        }
    ]
    
    strategies = []
    owner_idx = 0
    
    for data in strategies_data:
        ministry = data.pop("ministry")
        strategy = Strategy(
            **data,
            ministry_id=ministry.id,
            owner_id=owners[owner_idx].id,
            status=StrategyStatus.ACTIVE
        )
        db.add(strategy)
        strategies.append(strategy)
        owner_idx += 2  # Use every other owner
    
    db.commit()
    for strategy in strategies:
        db.refresh(strategy)
    print(f"✓ Created {len(strategies)} strategies")
    return strategies


def seed_milestones(db: Session, strategies: list):
    """Seed milestones"""
    print("\nSeeding milestones...")
    
    milestones_per_strategy = [
        # Green Hydrogen Strategy
        [
            ("Feasibility Study Completion", "Complete comprehensive feasibility study for green hydrogen production", date(2024, 12, 31), MilestoneStatus.COMPLETED, 100),
            ("Investor Engagement", "Secure commitments from international investors", date(2025, 6, 30), MilestoneStatus.IN_PROGRESS, 75),
            ("Infrastructure Planning", "Complete planning for port and pipeline infrastructure", date(2025, 12, 31), MilestoneStatus.IN_PROGRESS, 45),
            ("Regulatory Framework", "Establish regulatory framework for hydrogen industry", date(2026, 6, 30), MilestoneStatus.IN_PROGRESS, 30),
            ("Pilot Project Launch", "Launch first pilot green hydrogen production facility", date(2027, 12, 31), MilestoneStatus.NOT_STARTED, 0),
        ],
        # Food Security Plan
        [
            ("Baseline Assessment", "Complete baseline food security assessment", date(2024, 9, 30), MilestoneStatus.COMPLETED, 100),
            ("Irrigation Infrastructure", "Develop irrigation systems in key agricultural areas", date(2025, 12, 31), MilestoneStatus.IN_PROGRESS, 60),
            ("Farmer Training Programs", "Train 5,000 smallholder farmers in modern techniques", date(2026, 6, 30), MilestoneStatus.IN_PROGRESS, 40),
            ("Value Chain Development", "Establish agricultural value chains and market linkages", date(2027, 12, 31), MilestoneStatus.NOT_STARTED, 10),
        ],
        # Universal Health Coverage
        [
            ("Policy Framework", "Develop and approve UHC policy framework", date(2024, 12, 31), MilestoneStatus.COMPLETED, 100),
            ("Healthcare Facilities Upgrade", "Upgrade 50 primary healthcare facilities", date(2025, 12, 31), MilestoneStatus.IN_PROGRESS, 55),
            ("Health Insurance Scheme", "Launch national health insurance scheme", date(2026, 6, 30), MilestoneStatus.IN_PROGRESS, 35),
            ("Healthcare Workforce Training", "Train 1,000 additional healthcare workers", date(2027, 12, 31), MilestoneStatus.IN_PROGRESS, 25),
        ],
        # Digital Education
        [
            ("Digital Infrastructure", "Install internet connectivity in 200 schools", date(2025, 6, 30), MilestoneStatus.IN_PROGRESS, 50),
            ("Device Procurement", "Procure 50,000 tablets for students", date(2025, 12, 31), MilestoneStatus.IN_PROGRESS, 40),
            ("Teacher Training", "Train 3,000 teachers in digital pedagogy", date(2026, 6, 30), MilestoneStatus.NOT_STARTED, 15),
            ("Digital Content Development", "Develop digital curriculum content", date(2027, 12, 31), MilestoneStatus.NOT_STARTED, 5),
        ],
        # Wildlife Conservation
        [
            ("Conservation Areas Designation", "Designate new conservation areas", date(2025, 3, 31), MilestoneStatus.IN_PROGRESS, 70),
            ("Community Training", "Train 500 community members in tourism management", date(2025, 12, 31), MilestoneStatus.IN_PROGRESS, 45),
            ("Tourism Infrastructure", "Develop community tourism lodges and facilities", date(2026, 12, 31), MilestoneStatus.NOT_STARTED, 20),
            ("Wildlife Monitoring System", "Implement digital wildlife monitoring system", date(2027, 6, 30), MilestoneStatus.NOT_STARTED, 10),
        ]
    ]
    
    officers = ["John Mukwena", "Sarah Nghidinwa", "David Shapwa", "Maria Amakali", "Peter Hamunyela"]
    
    all_milestones = []
    for i, strategy in enumerate(strategies):
        for j, (title, desc, target, status, completion) in enumerate(milestones_per_strategy[i]):
            milestone = Milestone(
                strategy_id=strategy.id,
                title=title,
                description=desc,
                target_date=target,
                responsible_officer=officers[i],
                status=status,
                completion_percentage=completion,
                order_index=j
            )
            db.add(milestone)
            all_milestones.append(milestone)
    
    db.commit()
    print(f"✓ Created {len(all_milestones)} milestones")
    return all_milestones


def seed_progress_updates(db: Session, strategies: list, users: list):
    """Seed progress updates"""
    print("\nSeeding progress updates...")
    
    updates_data = [
        # Green Hydrogen - 2 updates
        [
            {
                "update_period": "Q2 2024",
                "overall_status": OverallStatus.GREEN,
                "completion_percentage": 45,
                "achievements": "• Completed comprehensive feasibility study\n• Signed 3 MoUs with international investors\n• Completed environmental impact assessment",
                "challenges": "• Awaiting approval of regulatory framework from Cabinet\n• Some delays in land acquisition process",
                "mitigation_measures": "• Expediting Cabinet approval process\n• Working with land commission on expedited acquisitions",
                "next_steps": "• Finalize investor agreements\n• Begin infrastructure planning\n• Complete regulatory framework",
                "published_date": datetime(2024, 7, 15)
            },
            {
                "update_period": "Q3 2024",
                "overall_status": OverallStatus.GREEN,
                "completion_percentage": 58,
                "achievements": "• Secured EUR 4.5 billion in investor commitments\n• Completed port infrastructure planning\n• Regulatory framework submitted to Parliament",
                "challenges": "• Pipeline route requires additional environmental assessments",
                "mitigation_measures": "• Fast-tracking environmental assessment process\n• Engaging environmental experts for rapid review",
                "next_steps": "• Parliamentary approval of regulatory framework\n• Begin tendering for infrastructure construction\n• Launch workforce training program",
                "published_date": datetime(2024, 10, 15)
            }
        ],
        # Food Security - 2 updates
        [
            {
                "update_period": "Q2 2024",
                "overall_status": OverallStatus.AMBER,
                "completion_percentage": 35,
                "achievements": "• Baseline food security assessment completed\n• 15 irrigation systems installed in Kavango regions\n• 2,000 farmers trained in modern techniques",
                "challenges": "• Drought conditions affecting implementation timeline\n• Equipment procurement delays from suppliers",
                "mitigation_measures": "• Adjusted implementation timeline for drought conditions\n• Identified alternative equipment suppliers\n• Implementing drought-resistant crop programs",
                "next_steps": "• Continue irrigation infrastructure development\n• Expand farmer training program\n• Launch seed distribution program",
                "published_date": datetime(2024, 7, 20)
            },
            {
                "update_period": "Q3 2024",
                "overall_status": OverallStatus.AMBER,
                "completion_percentage": 42,
                "achievements": "• Additional 10 irrigation systems installed\n• Trained 1,500 more farmers (total 3,500)\n• Distributed drought-resistant seeds to 5,000 farmers",
                "challenges": "• Continued drought impacting crop yields\n• Slower than expected farmer adoption rates",
                "mitigation_measures": "• Increased extension services support\n• Providing additional drought relief support\n• Enhancing farmer education programs",
                "next_steps": "• Install remaining 25 irrigation systems\n• Reach 5,000 farmer training target\n• Begin value chain development",
                "published_date": datetime(2024, 10, 20)
            }
        ],
        # Universal Health Coverage - 1 update
        [
            {
                "update_period": "Q3 2024",
                "overall_status": OverallStatus.GREEN,
                "completion_percentage": 48,
                "achievements": "• UHC policy framework approved by Cabinet\n• 28 healthcare facilities upgraded\n• Health insurance scheme design completed\n• Recruited 350 new healthcare workers",
                "challenges": "• Some facilities experiencing construction delays\n• Healthcare worker retention in rural areas",
                "mitigation_measures": "• Providing rural allowances for healthcare workers\n• Accelerating construction timelines\n• Implementing retention incentives",
                "next_steps": "• Complete remaining 22 facility upgrades\n• Launch health insurance enrollment campaign\n• Continue healthcare workforce recruitment",
                "published_date": datetime(2024, 10, 25)
            }
        ]
    ]
    
    owners = [u for u in users if u.role == UserRole.STRATEGY_OWNER]
    
    all_updates = []
    strategy_indices = [0, 1, 2]  # First 3 strategies get updates
    
    for idx, strategy_idx in enumerate(strategy_indices):
        strategy = strategies[strategy_idx]
        for update_data in updates_data[idx]:
            update = ProgressUpdate(
                strategy_id=strategy.id,
                user_id=strategy.owner_id,
                **update_data
            )
            db.add(update)
            all_updates.append(update)
    
    db.commit()
    print(f"✓ Created {len(all_updates)} progress updates")
    return all_updates


def seed_questions(db: Session, strategies: list):
    """Seed questions and responses"""
    print("\nSeeding questions...")
    
    questions_data = [
        # Green Hydrogen
        [
            ("When will the first green hydrogen production begin?", "Initial production is targeted for Q2 2028, following completion of the pilot facility.", True),
            ("How many jobs will be created by this strategy?", "We estimate the creation of approximately 15,000 direct jobs and 30,000 indirect jobs over the implementation period.", True),
            ("What environmental protections are in place?", "Comprehensive environmental impact assessments have been completed, and all production will comply with international environmental standards.", True),
        ],
        # Food Security
        [
            ("How will small-scale farmers benefit from this plan?", "Small-scale farmers will receive free training, subsidized irrigation equipment, and access to improved seeds. We're also establishing market linkages to ensure fair prices.", True),
            ("What is being done about the current drought?", "We've distributed drought-resistant seeds to 5,000 farmers and are accelerating irrigation infrastructure development. Emergency food assistance is also available.", True),
        ],
        # Health Coverage
        [
            ("When can citizens start enrolling in the health insurance?", "The health insurance enrollment campaign will launch in Q2 2025. More information will be available on our website.", True),
            ("Will the insurance cover pre-existing conditions?", "Yes, the national health insurance scheme will provide universal coverage including pre-existing conditions.", True),
        ],
        # Digital Education
        [
            ("Which schools will receive tablets first?", None, False),  # Pending moderation
        ],
        # Wildlife Conservation
        [
            ("How can communities participate in tourism activities?", None, False),  # Pending moderation
        ]
    ]
    
    all_questions = []
    submitter_names = ["John Namwandi", "Maria Sheehama", "David Kamwi", "Sarah Nambala", "Anonymous", "Peter Shilongo", "Grace Nauyoma"]
    
    for i, strategy in enumerate(strategies[:5]):
        if i < len(questions_data):
            for j, (question_text, response_text, is_published) in enumerate(questions_data[i]):
                question = Question(
                    strategy_id=strategy.id,
                    question_text=question_text,
                    submitter_name=submitter_names[len(all_questions) % len(submitter_names)] if len(all_questions) % 3 != 0 else None,
                    submitter_email=f"citizen{len(all_questions)+1}@example.com" if len(all_questions) % 2 == 0 else None,
                    status=QuestionStatus.PUBLISHED if is_published else QuestionStatus.PENDING_MODERATION,
                    submitted_at=datetime.now() - timedelta(days=random.randint(1, 30)),
                    response_text=response_text,
                    response_published_at=datetime.now() - timedelta(days=random.randint(1, 15)) if response_text else None
                )
                db.add(question)
                all_questions.append(question)
    
    db.commit()
    print(f"✓ Created {len(all_questions)} questions")
    return all_questions


def seed_audit_logs(db: Session, users: list):
    """Seed some audit log entries"""
    print("\nSeeding audit logs...")
    
    actions = [
        "USER_LOGIN",
        "STRATEGY_CREATED",
        "PROGRESS_UPDATE_SUBMITTED",
        "QUESTION_SUBMITTED",
        "QUESTION_MODERATED"
    ]
    
    logs = []
    for i in range(20):
        user = random.choice(users)
        log = AuditLog(
            user_id=user.id,
            action=random.choice(actions),
            entity_type="various",
            ip_address=f"192.168.1.{random.randint(1, 255)}",
            user_agent="Mozilla/5.0...",
            timestamp=datetime.now() - timedelta(days=random.randint(0, 30))
        )
        db.add(log)
        logs.append(log)
    
    db.commit()
    print(f"✓ Created {len(logs)} audit log entries")
    return logs


def main():
    """Main seeding function"""
    print("=" * 60)
    print("DATABASE SEEDING SCRIPT")
    print("National Strategy Transparency Platform")
    print("=" * 60)
    
    # Create tables
    create_tables()
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Seed data in order (respecting foreign key constraints)
        ministries = seed_ministries(db)
        users = seed_users(db, ministries)
        strategies = seed_strategies(db, ministries, users)
        milestones = seed_milestones(db, strategies)
        progress_updates = seed_progress_updates(db, strategies, users)
        questions = seed_questions(db, strategies)
        audit_logs = seed_audit_logs(db, users)
        
        print("\n" + "=" * 60)
        print("SEEDING COMPLETE!")
        print("=" * 60)
        print("\nSummary:")
        print(f"  - Ministries: {len(ministries)}")
        print(f"  - Users: {len(users)}")
        print(f"  - Strategies: {len(strategies)}")
        print(f"  - Milestones: {len(milestones)}")
        print(f"  - Progress Updates: {len(progress_updates)}")
        print(f"  - Questions: {len(questions)}")
        print(f"  - Audit Logs: {len(audit_logs)}")
        print("\nDefault Credentials:")
        print("  - Platform Admin: admin@gov.na / Admin@123456")
        print("  - Ministry Admin: admin.mme@gov.na / Admin@123456")
        print("  - Strategy Owner: owner1.mme@gov.na / Owner@123456")
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
