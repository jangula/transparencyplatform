#!/bin/bash

# National Strategy Transparency Platform - Startup Script
# This script starts both backend and frontend services

echo "🚀 Starting National Strategy Transparency Platform..."
echo ""

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if backend is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Backend already running on port 8000${NC}"
else
    echo -e "${BLUE}📡 Starting Backend API...${NC}"
    cd "$SCRIPT_DIR/backend"
    source venv/bin/activate
    nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/nstp_backend.log 2>&1 &
    BACKEND_PID=$!
    echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"
    echo "  - API: http://localhost:8000"
    echo "  - Docs: http://localhost:8000/docs"
    echo "  - Logs: /tmp/nstp_backend.log"
fi

echo ""

# Check if frontend is already running
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}⚠️  Frontend already running on port 3000${NC}"
else
    echo -e "${BLUE}🎨 Starting Frontend App...${NC}"
    cd "$SCRIPT_DIR/frontend"
    nohup npm start > /tmp/nstp_frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"
    echo "  - App: http://localhost:3000"
    echo "  - Logs: /tmp/nstp_frontend.log"
fi

echo ""
echo -e "${GREEN}✅ System startup initiated!${NC}"
echo ""
echo "Waiting for services to be ready..."
sleep 8

# Check if services are responding
echo ""
echo "🔍 Checking services..."

if curl -s http://localhost:8000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Backend API is responding${NC}"
else
    echo -e "${YELLOW}⚠️  Backend API not responding yet (may need more time)${NC}"
fi

if curl -s http://localhost:3000/ > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend is responding${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend not responding yet (may need more time)${NC}"
    echo "   Frontend typically takes 30-60 seconds to fully start"
fi

echo ""
echo "📋 Default Login Credentials:"
echo "  Platform Admin: admin@gov.na / Admin@123456"
echo "  Ministry Admin: admin.mme@gov.na / Admin@123456"
echo "  Strategy Owner: owner1.mme@gov.na / Owner@123456"
echo ""
echo "🌐 Access Points:"
echo "  • Frontend: http://localhost:3000"
echo "  • Backend API: http://localhost:8000"
echo "  • API Documentation: http://localhost:8000/docs"
echo ""
echo "To stop the system, run: ./STOP_SYSTEM.sh"
echo ""
