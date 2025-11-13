# System Startup Commands

## Quick Start (Recommended)

### Using the startup script:
```bash
cd /Users/angula/Desktop/transparencyplatform
./START_SYSTEM.sh
```

### To stop the system:
```bash
./STOP_SYSTEM.sh
```

---

## Manual Startup Commands

If you prefer to start services manually in separate terminal windows:

### Terminal 1 - Backend API

```bash
# Navigate to backend directory
cd /Users/angula/Desktop/transparencyplatform/backend

# Activate Python virtual environment
source venv/bin/activate

# Start the backend server
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Backend will be available at:**
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Docs: http://localhost:8000/redoc

---

### Terminal 2 - Frontend Application

```bash
# Navigate to frontend directory
cd /Users/angula/Desktop/transparencyplatform/frontend

# Start the React development server
npm start
```

**Frontend will be available at:**
- Application: http://localhost:3000

---

## Background Mode (Without Terminal Windows)

### Start Backend in Background
```bash
cd /Users/angula/Desktop/transparencyplatform/backend
source venv/bin/activate
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/backend.log 2>&1 &
```

### Start Frontend in Background
```bash
cd /Users/angula/Desktop/transparencyplatform/frontend
nohup npm start > /tmp/frontend.log 2>&1 &
```

### View Logs
```bash
# Backend logs
tail -f /tmp/backend.log

# Frontend logs
tail -f /tmp/frontend.log
```

---

## Stop Services Manually

### Stop Backend
```bash
# Find and kill the process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Stop Frontend
```bash
# Find and kill the process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## Check if Services are Running

```bash
# Check backend
curl http://localhost:8000/

# Check frontend
curl http://localhost:3000/

# Or check ports
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
```

---

## Default Login Credentials

After the system starts, you can login with:

### Platform Administrator
- **Email:** admin@gov.na
- **Password:** Admin@123456
- **Access:** Full system access

### Ministry Administrator (Mines & Energy)
- **Email:** admin.mme@gov.na
- **Password:** Admin@123456
- **Access:** Ministry management

### Strategy Owner
- **Email:** owner1.mme@gov.na
- **Password:** Owner@123456
- **Access:** Strategy updates

---

## Troubleshooting

### Port Already in Use
If you get "port already in use" errors:

```bash
# Kill processes on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill processes on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### Backend Won't Start
```bash
# Check database connection
cd /Users/angula/Desktop/transparencyplatform/backend
source venv/bin/activate
python -c "from app.db.session import engine; print('DB Connected:', engine.url)"

# Check if PostgreSQL is running
ps aux | grep postgres
```

### Frontend Won't Start
```bash
# Reinstall dependencies
cd /Users/angula/Desktop/transparencyplatform/frontend
rm -rf node_modules
npm install
npm start
```

### View Real-time Logs
```bash
# Backend (if started in background)
tail -f /tmp/backend.log

# Frontend (if started in background)
tail -f /tmp/frontend.log
```

---

## Database Management

### Seed the Database
```bash
cd /Users/angula/Desktop/transparencyplatform/backend
source venv/bin/activate
python scripts/seed_database.py
```

### Connect to Database
```bash
psql postgresql://nstp_user:nstp_password@localhost:5432/transparency_platform
```

---

## System Requirements

- **Python:** 3.13+
- **Node.js:** 14+
- **PostgreSQL:** 15+
- **Operating System:** macOS, Linux, or WSL on Windows

---

## Quick Reference

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Public web interface |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| ReDoc | http://localhost:8000/redoc | Alternative API documentation |

---

**For the simplest startup experience, just run:**
```bash
./START_SYSTEM.sh
```

**And to stop:**
```bash
./STOP_SYSTEM.sh
```
