# Quick Reference Guide
## National Strategy Transparency Platform

This is a quick reference for common development tasks.

## 🚀 Quick Start

```bash
# Start everything with Docker
docker-compose up -d

# Create admin user
docker-compose exec backend python scripts/create_admin.py

# View logs
docker-compose logs -f backend
```

## 🔧 Development Commands

### Backend

```bash
# Start development server
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Install new package
pip install package-name
pip freeze > requirements.txt

# Run tests
pytest
pytest --cov=app
pytest tests/test_auth.py -v

# Code formatting
black app/
isort app/
flake8 app/

# Type checking
mypy app/
```

### Database

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Show current version
alembic current

# Reset database (⚠️ destroys data)
dropdb transparency_platform
createdb transparency_platform
alembic upgrade head
```

### Docker

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild containers
docker-compose build

# View logs
docker-compose logs -f backend
docker-compose logs -f postgres

# Execute command in container
docker-compose exec backend bash
docker-compose exec postgres psql -U nstp_user -d transparency_platform

# Stop and remove volumes (⚠️ destroys data)
docker-compose down -v
```

### Frontend (when built)

```bash
# Start development server
cd frontend
npm start

# Install package
npm install package-name

# Build for production
npm run build

# Run tests
npm test
npm run test:coverage
```

## 🔍 Testing the API

### Using cURL

```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gov.na","password":"Admin@123456"}'

# Get current user
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Health check
curl http://localhost:8000/health
```

### Using HTTPie (cleaner syntax)

```bash
# Install httpie
pip install httpie

# Login
http POST localhost:8000/api/v1/auth/login email=admin@gov.na password=Admin@123456

# Get current user
http GET localhost:8000/api/v1/auth/me Authorization:"Bearer YOUR_TOKEN"
```

### Using Swagger UI (Recommended)

1. Open http://localhost:8000/docs
2. Click "Authorize" button
3. Enter `Bearer YOUR_TOKEN`
4. Test endpoints interactively

## 📊 Database Commands

### PostgreSQL

```bash
# Connect to database
psql -U nstp_user -d transparency_platform

# List databases
\l

# List tables
\dt

# Describe table
\d users

# Run query
SELECT * FROM users LIMIT 10;

# Exit
\q
```

### Common SQL Queries

```sql
-- Count users by role
SELECT role, COUNT(*) FROM users GROUP BY role;

-- List strategies with ministry
SELECT s.title, m.name FROM strategies s 
JOIN ministries m ON s.ministry_id = m.id;

-- Find overdue updates
SELECT * FROM strategies WHERE id NOT IN (
  SELECT strategy_id FROM progress_updates 
  WHERE published_date > NOW() - INTERVAL '3 months'
);

-- Recent audit logs
SELECT * FROM audit_logs ORDER BY timestamp DESC LIMIT 20;
```

## 🐛 Debugging

### Check Logs

```bash
# Backend logs
tail -f backend/logs/app.log

# Docker logs
docker-compose logs -f backend

# Specific level
grep "ERROR" backend/logs/app.log
```

### Common Issues

**Database connection failed:**
```bash
# Check PostgreSQL is running
pg_isready -U nstp_user

# Verify DATABASE_URL in .env
cat backend/.env | grep DATABASE_URL
```

**Port already in use:**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Module not found:**
```bash
# Verify virtual environment
which python

# Reinstall dependencies
pip install -r requirements.txt
```

## 🔐 Security Commands

### Generate Secret Key

```bash
# For SECRET_KEY in .env
python -c "import secrets; print(secrets.token_hex(32))"

# For JWT secret
openssl rand -hex 32
```

### Create User

```bash
# Using script
python backend/scripts/create_admin.py

# Using API (requires auth token)
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email":"user@ministry.gov.na",
    "password":"SecurePass123!",
    "first_name":"John",
    "last_name":"Doe",
    "role":"STRATEGY_OWNER"
  }'
```

## 📦 Deployment Commands

### Production Build

```bash
# Backend - already containerized
docker build -t nstp-backend:latest ./backend

# Frontend (when built)
cd frontend
npm run build
```

### Environment Setup

```bash
# Copy production env
cp backend/.env.example backend/.env.production

# Generate secrets
python -c "import secrets; print(f'SECRET_KEY={secrets.token_hex(32)}')" >> backend/.env.production
```

### Database Backup

```bash
# Backup database
pg_dump -U nstp_user transparency_platform > backup_$(date +%Y%m%d).sql

# Restore database
psql -U nstp_user transparency_platform < backup_20251111.sql

# Docker backup
docker-compose exec postgres pg_dump -U nstp_user transparency_platform > backup.sql
```

## 📈 Monitoring

### Health Checks

```bash
# Application health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/health/db

# Docker health
docker-compose ps
```

### Performance

```bash
# Monitor database queries
# Add to .env: LOG_LEVEL=DEBUG

# Monitor requests
tail -f backend/logs/app.log | grep "Process-Time"
```

## 🧪 Testing

### Run Specific Tests

```bash
# Auth tests only
pytest tests/test_auth.py

# With output
pytest -v -s

# Stop on first failure
pytest -x

# Run parallel
pytest -n 4
```

### Test Coverage

```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

## 🔄 Git Workflow

```bash
# Create feature branch
git checkout -b feature/my-feature

# Commit changes
git add .
git commit -m "Add: My feature"

# Push branch
git push origin feature/my-feature

# Update from main
git checkout main
git pull
git checkout feature/my-feature
git rebase main
```

## 🎨 Code Quality

```bash
# Format all code
black app/ tests/
isort app/ tests/

# Check code quality
flake8 app/
pylint app/
mypy app/

# Pre-commit checks (create hook)
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
black app/ --check
flake8 app/
pytest
EOF
chmod +x .git/hooks/pre-commit
```

## 📚 Documentation

```bash
# Generate API docs (automatic with FastAPI)
# Visit: http://localhost:8000/docs

# Update requirements
pip freeze > requirements.txt

# Generate ERD (entity relationship diagram)
# Install: pip install eralchemy
eralchemy -i 'postgresql://nstp_user:password@localhost/transparency_platform' -o erd.png
```

## 🚨 Emergency Commands

```bash
# Stop everything
docker-compose down
pkill -f uvicorn

# Reset database
docker-compose down -v
docker-compose up -d
docker-compose exec backend alembic upgrade head

# Clear Redis cache
docker-compose exec redis redis-cli FLUSHALL

# Restore from backup
docker-compose exec -T postgres psql -U nstp_user transparency_platform < backup.sql
```

## 📞 Get Help

```bash
# Python help
python -m pydoc app.core.security

# Docker help
docker-compose --help
docker-compose logs --help

# Alembic help
alembic --help
alembic upgrade --help
```

---

**Pro Tips:**

1. **Use aliases** in your `.bashrc` or `.zshrc`:
   ```bash
   alias dc='docker-compose'
   alias dce='docker-compose exec'
   alias dcl='docker-compose logs -f'
   ```

2. **Use direnv** for automatic environment loading:
   ```bash
   # Install direnv, then:
   echo "source venv/bin/activate" > .envrc
   direnv allow
   ```

3. **Use httpie** instead of curl for cleaner API testing

4. **Keep Swagger UI open** at http://localhost:8000/docs for interactive testing

---

**Quick Links:**
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Database: postgresql://nstp_user@localhost:5432/transparency_platform
