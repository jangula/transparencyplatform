#!/bin/bash

# National Strategy Transparency Platform - Shutdown Script
# This script stops both backend and frontend services

echo "🛑 Stopping National Strategy Transparency Platform..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Stop backend (port 8000)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Stopping Backend API (port 8000)...${NC}"
    lsof -ti:8000 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓ Backend stopped${NC}"
else
    echo -e "${YELLOW}Backend not running${NC}"
fi

echo ""

# Stop frontend (port 3000)
if lsof -Pi :3000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo -e "${YELLOW}Stopping Frontend (port 3000)...${NC}"
    lsof -ti:3000 | xargs kill -9 2>/dev/null
    echo -e "${GREEN}✓ Frontend stopped${NC}"
else
    echo -e "${YELLOW}Frontend not running${NC}"
fi

echo ""
echo -e "${GREEN}✅ System stopped${NC}"
echo ""
