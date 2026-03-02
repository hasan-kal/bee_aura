#!/bin/bash
# Quick Start Script for ERP Ticket Triaging System
# This script sets up the environment and runs the application

set -e  # Exit on error

echo "🎯 ERP Ticket Triaging System - Quick Start"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python installation..."
python3 --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "✓ Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# Install/upgrade dependencies
echo "✓ Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1

# Check for API key
echo ""
echo "⚙️  Configuration Check"
echo "======================="
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY environment variable not set"
    echo "   You can:"
    echo "   1. Set it now: export OPENAI_API_KEY='sk-...'"
    echo "   2. Enter it in the app UI when prompted"
    echo "   3. Add to .streamlit/secrets.toml for permanent setup"
else
    echo "✓ OPENAI_API_KEY is configured"
fi

echo ""
echo "🚀 Starting application..."
echo "   Application will open at: http://localhost:8501"
echo "   Press Ctrl+C to stop"
echo ""

# Run the application
streamlit run app.py
