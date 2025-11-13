#!/usr/bin/env python
"""
Create initial platform administrator
Run this script after setting up the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from datetime import datetime, timedelta
import uuid


def create_admin():
    """Create platform administrator"""
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.email == "admin@gov.na").first()
        
        if admin:
            print("❌ Admin user already exists!")
            print(f"   Email: {admin.email}")
            print(f"   Created: {admin.created_at}")
            return
        
        # Get admin details
        print("=" * 60)
        print("CREATE PLATFORM ADMINISTRATOR")
        print("=" * 60)
        
        email = input("Admin email [admin@gov.na]: ").strip() or "admin@gov.na"
        first_name = input("First name [Platform]: ").strip() or "Platform"
        last_name = input("Last name [Administrator]: ").strip() or "Administrator"
        password = input("Password [Admin@123456]: ").strip() or "Admin@123456"
        
        # Create admin user
        admin = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            role=UserRole.PLATFORM_ADMIN,
            is_active=True,
            mfa_enabled=False,
            password_changed_at=datetime.utcnow(),
            password_expires_at=datetime.utcnow() + timedelta(days=90)
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print("\n" + "=" * 60)
        print("✅ ADMIN USER CREATED SUCCESSFULLY!")
        print("=" * 60)
        print(f"Email:    {admin.email}")
        print(f"Password: {password}")
        print(f"Role:     {admin.role}")
        print(f"User ID:  {admin.id}")
        print("=" * 60)
        print("\n⚠️  IMPORTANT: Change this password immediately after first login!")
        print("   Use: POST /api/v1/auth/password/change\n")
        
    except Exception as e:
        print(f"❌ Error creating admin: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()
