@echo off
setlocal enabledelayedexpansion

REM Claude Code RAG Chatbot Startup Script for Windows

echo.
echo ================================================
echo Claude Code RAG Chatbot
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo.
    echo Steps to get started:
    echo 1. Copy .env.example to .env
    echo 2. Add your ANTHROPIC_API_KEY to .env
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

REM Check if requirements are installed
pip show fastapi >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    echo This may take a few minutes on first run...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check for API key
for /f "usebackq delims==" %%I in (`findstr /R "ANTHROPIC_API_KEY" .env`) do (
    set line=%%I
    if "!line!"=="" (
        echo ERROR: ANTHROPIC_API_KEY not set in .env
        pause
        exit /b 1
    )
)

echo.
echo Starting Claude Code RAG Chatbot...
echo.
echo ================================================
echo Server will run at: http://localhost:8000
echo ================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
