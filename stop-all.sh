#!/bin/bash

# Hack-Aura Stop Script
# This script stops ALL running services

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         Stopping Hack-Aura AI Company                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

echo "🛑 Stopping all services..."
echo ""

# Stop Node.js processes
echo "▶ Stopping Backend & Frontend..."
pkill -f "node server.js"
pkill -f "react-scripts"
pkill -f "npm run dev"

# Stop Python uAgents
echo "▶ Stopping AI uAgents..."
pkill -f "ceo_uagent.py"
pkill -f "research_uagent.py"
pkill -f "product_uagent.py"
pkill -f "cmo_uagent.py"
pkill -f "cto_uagent.py"
pkill -f "head_engineering_uagent.py"
pkill -f "finance_uagent.py"
pkill -f "orchestrator_uagent.py"
pkill -f "research_metta_uagent.py"

sleep 2

echo ""
echo "✅ All services stopped!"
echo ""
echo "💡 To start again, run: ./start-all.sh"
echo ""

