#!/bin/bash

# Hack-Aura Complete Startup Script
# This script starts ALL services needed for the AI company

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         Starting Hack-Aura AI Company                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the hack-aura directory"
    exit 1
fi

echo "🚀 Starting services..."
echo ""

# Start Backend Server
echo "▶ Starting Backend Server (Port 5001)..."
PORT=5001 npm start > /dev/null 2>&1 &
sleep 2

# Start Frontend Client
echo "▶ Starting Frontend Client (Port 3001)..."
cd client && REACT_APP_API_URL=http://localhost:5001 PORT=3001 npm start > /dev/null 2>&1 &
cd ..
sleep 3

# Start Bolt.diy
echo "▶ Starting Bolt.diy (Port 5173)..."
cd bolt.diy-main && npm run dev > /dev/null 2>&1 &
cd ..
sleep 2

# Start AI uAgents
echo "▶ Starting AI uAgents..."
cd ai_uagents

echo "  • CEO Agent (8001)..."
python3 ceo_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • Research Agent (8002)..."
python3 research_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • Product Agent (8003)..."
python3 product_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • CMO Agent (8004)..."
python3 cmo_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • CTO Agent (8005)..."
python3 cto_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • Head of Engineering (8006)..."
python3 head_engineering_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • Finance Agent (8007)..."
python3 finance_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • Orchestrator (8008)..."
python3 orchestrator_uagent.py > /dev/null 2>&1 &
sleep 1

echo "  • MeTTa Research Agent (8009) - CRITICAL..."
python3 research_metta_uagent.py > /dev/null 2>&1 &
sleep 2

cd ..

echo ""
echo "⏳ Waiting for all services to start..."
sleep 5

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              ✅ ALL SERVICES STARTED!                    ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Access your AI Company at:"
echo "   • Frontend:  http://localhost:3001"
echo "   • Backend:   http://localhost:5001"
echo "   • Bolt.diy:  http://localhost:5173"
echo ""
echo "🤖 AI Agents running on ports 8001-8009"
echo ""
echo "💡 Tip: To stop all services, run: ./stop-all.sh"
echo ""

