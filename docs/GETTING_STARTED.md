# Getting Started Guide
## National Strategy Transparency Platform

This guide will help you set up and run the National Strategy Transparency Platform locally for development.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11+** - [Download Python](https://www.python.org/downloads/)
- **PostgreSQL 15.x** - [Download PostgreSQL](https://www.postgresql.org/download/)
- **Node.js 20.x LTS** - [Download Node.js](https://nodejs.org/) (for frontend)
- **Docker & Docker Compose** (Optional but recommended) - [Download Docker](https://www.docker.com/products/docker-desktop/)
- **Git** - [Download Git](https://git-scm.com/downloads)

## Option 1: Quick Start with Docker (Recommended)

This is the fastest way to get the platform running.

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd transparencyplatform
```

### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp backend/.env.example backend/.env

# Edit the .env file with your settings
# For local development, the defaults should work
```

### Step 3: Start All Services

```bash
# Start PostgreSQL, Redis, Backend, and Frontend
docker-compose up -d

# View logs
docker-compose logs -f backend
```

### Step 4: Initialize the Database

```bash
# Run database migrations
docker-compose exec backend alembic upgrade head

# Create initial admin user
docker-compose exec backend python scripts/create_admin.py
```

### Step 5: Access the Application

- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000 (once implemented)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### Stopping Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (warning: deletes data)
docker-compose down -v
```

## Option 2: Manual Setup (Development)

If you prefer to run services individually for development.

### Step 1: Setup PostgreSQL Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE transparency_platform;
CREATE USER nstp_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE transparency_platform TO nstp_user;
\q
```

### Step 2: Setup Python Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials
```

**Edit backend/.env:**
```env
DATABASE_URL=postgresql://nstp_user:your_password@localhost:5432/transparency_platform
SECRET_KEY=your-secret-key-generate-with-openssl-rand-hex-32
```

### Step 3: Generate Secret Key

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"

# Copy the output and paste it in your .env file as SECRET_KEY
```

### Step 4: Initialize Database

```bash
# Initialize Alembic (first time only)
alembic init alembic

# Or if Alembic is already configured, run migrations
alembic upgrade head

# Create initial data
python scripts/seed_data.py
```

### Step 5: Start Backend Server

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using Python directly
python -m app.main
```

The backend will be available at http://localhost:8000

### Step 6: Verify Backend is Running

Open your browser and visit:
- http://localhost:8000 - Should show welcome message
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/health - Health check

### Step 7: Setup Frontend (When Available)

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Start development server
npm start
```

The frontend will be available at http://localhost:3000

## Creating Your First Admin User

### Option 1: Using Python Script

```bash
cd backend
source venv/bin/activate  # If not already activated

# Create the script
cat > scripts/create_admin.py << 'EOF'
import sys
sys.path.append('.')

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash
import uuid

db = SessionLocal()

# Check if admin exists
admin = db.query(User).filter(User.email == "admin@gov.na").first()
if admin:
    print("Admin user already exists!")
else:
    admin = User(
        id=uuid.uuid4(),
        email="admin@gov.na",
        password_hash=get_password_hash("Admin@123456"),
        first_name="Platform",
        last_name="Administrator",
        role="PLATFORM_ADMIN",
        is_active=True,
        mfa_enabled=False
    )
    db.add(admin)
    db.commit()
    print(f"Admin user created: {admin.email}")
    print("Password: Admin@123456")
    print("IMPORTANT: Change this password immediately after first login!")

db.close()
EOF

# Run the script
python scripts/create_admin.py
```

Default admin credentials:
- Email: admin@gov.na
- Password: Admin@123456
- **⚠️ CHANGE THIS PASSWORD IMMEDIATELY AFTER FIRST LOGIN**

### Option 2: Using API

```bash
# First, you need to have at least one admin user created manually
# Then you can use the /auth/register endpoint to create more users

curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@ministry.gov.na",
    "password": "SecurePassword123!",
    "first_name": "John",
    "last_name": "Doe",
    "role": "STRATEGY_OWNER",
    "ministry_id": "ministry-uuid-here"
  }'
```

## Testing the API

### 1. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@gov.na",
    "password": "Admin@123456"
  }'
```

You'll receive a response with access_token and refresh_token.

### 2. Get Current User Info

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs
2. Click "Authorize" button (top right)
3. Enter: `Bearer YOUR_ACCESS_TOKEN`
4. Now you can test all endpoints interactively

## Common Development Tasks

### Viewing Logs

```bash
# Docker
docker-compose logs -f backend

# Manual setup
tail -f backend/logs/app.log
```

### Accessing Database

```bash
# Docker
docker-compose exec postgres psql -U nstp_user -d transparency_platform

# Manual
psql -U nstp_user -d transparency_platform
```

### Running Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py -v
```

### Creating Database Migrations

```bash
cd backend
source venv/bin/activate

# Create new migration
alembic revision --autogenerate -m "Add new column to users"

# Review the generated migration file
# Edit if needed: alembic/versions/xxx_add_new_column_to_users.py

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Resetting Database

```bash
# Docker
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head

# Manual
dropdb transparency_platform
createdb transparency_platform
alembic upgrade head
python scripts/seed_data.py
```

## Troubleshooting

### Issue: "Database connection failed"

**Solution:**
1. Check PostgreSQL is running: `psql -U postgres -c "SELECT 1"`
2. Verify DATABASE_URL in .env file
3. Ensure database exists: `psql -U postgres -c "\l"`
4. Check credentials are correct

### Issue: "ModuleNotFoundError: No module named 'app'"

**Solution:**
1. Ensure you're in the backend directory
2. Virtual environment is activated
3. Dependencies are installed: `pip install -r requirements.txt`
4. Try running with: `python -m uvicorn app.main:app`

### Issue: "Port 8000 already in use"

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or use a different port
uvicorn app.main:app --port 8001
```

### Issue: "alembic command not found"

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall alembic
pip install alembic
```

### Issue: Docker container keeps restarting

**Solution:**
```bash
# Check logs
docker-compose logs backend

# Common causes:
# 1. Database URL incorrect - check .env file
# 2. Missing SECRET_KEY - add to .env
# 3. Port conflict - change port in docker-compose.yml
```

## Environment Variables Reference

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@localhost:5432/db |
| SECRET_KEY | JWT signing key (32+ chars) | Use `openssl rand -hex 32` |
| SMTP_HOST | Email server host | smtp.sendgrid.net |
| SMTP_PASSWORD | Email server password | your-api-key |
| EMAIL_FROM | Sender email address | noreply@strategyprogress.gov.na |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DEBUG | Enable debug mode | true |
| LOG_LEVEL | Logging level | INFO |
| CORS_ORIGINS | Allowed origins | http://localhost:3000 |
| USE_S3 | Use AWS S3 for files | false |
| ENABLE_MFA | Enable MFA requirement | true |

## Next Steps

1. **Change default admin password** - Security first!
2. **Create ministries** - Use admin panel or API
3. **Create users** - Assign to ministries
4. **Upload sample strategies** - Test the system
5. **Submit progress updates** - Test workflow
6. **Ask questions** - Test Q&A feature

## Getting Help

- **API Documentation**: http://localhost:8000/docs
- **Technical Specification**: See `docs/` folder
- **Implementation Status**: See `docs/IMPLEMENTATION_STATUS.md`
- **Issues**: Check logs in `backend/logs/app.log`

## Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/my-feature

# 2. Make changes
# Edit files...

# 3. Test changes
pytest
python -m flake8 app/

# 4. Commit changes
git add .
git commit -m "Add: My new feature"

# 5. Push and create PR
git push origin feature/my-feature
```

## Code Quality Tools

```bash
# Format code with Black
black app/

# Sort imports
isort app/

# Lint code
flake8 app/
pylint app/

# Type checking
mypy app/
```

---

**Ready to develop!** 🚀

If you encounter any issues not covered here, check the logs or create an issue in the repository.
