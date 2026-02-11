#!/bin/bash

# Claude Code RAG Chatbot Startup Script for Linux/Mac

echo ""
echo "================================================"
echo "Claude Code RAG Chatbot"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo ""
    echo "Steps to get started:"
    echo "1. Copy .env.example to .env"
    echo "2. Add your ANTHROPIC_API_KEY to .env"
    echo "3. Run this script again"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if requirements are installed
python3 -c "import fastapi" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    echo "This may take a few minutes on first run..."
    echo ""
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        read -p "Press Enter to exit..."
        exit 1
    fi
fi

# Check for API key
if ! grep -q "ANTHROPIC_API_KEY" .env; then
    echo "ERROR: ANTHROPIC_API_KEY not found in .env"
    read -p "Press Enter to exit..."
    exit 1
fi

echo ""
echo "Starting Claude Code RAG Chatbot..."
echo ""
echo "================================================"
echo "Server will run at: http://localhost:8000"
echo "================================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 main.py

read -p "Press Enter to exit..."
