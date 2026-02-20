@echo off
REM Vibe Coder GUI Launcher for Windows
REM Double-click this file to open the GUI

title Vibe Coder - Autonomous App Factory

echo ========================================
echo   Vibe Coder - Starting GUI...
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo Virtual environment not found!
    echo Running setup...
    call setup.bat
    if %errorlevel% neq 0 (
        echo Setup failed!
        pause
        exit /b 1
    )
)

REM Activate virtual environment and run GUI
echo Starting GUI...
call venv\Scripts\activate.bat
python gui.py

REM If GUI exits, keep window open
echo.
echo GUI closed. Press any key to exit...
pause >nul
