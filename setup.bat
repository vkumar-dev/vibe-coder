@echo off
REM Vibe Coder Setup for Windows
REM Run this first to install dependencies

title Vibe Coder - Setup

echo ========================================
echo   Vibe Coder - Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Install from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Now you can run: run-gui.bat
echo.
pause
