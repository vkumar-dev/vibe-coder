@echo off
REM Vibe Coder - Autonomous App Factory
REM Double-click to start the GUI

title Vibe Coder

echo ========================================
echo   Vibe Coder - Starting...
echo ========================================
echo.

REM Get script directory
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

REM Convert to WSL path
set WSL_DIR=/home/eliza/qwen/vibe-coder

REM Run in WSL
wsl --cd "%WSL_DIR%" -e bash -c "./run-gui.sh"

if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo   Error starting Vibe Coder
    echo ========================================
    echo.
    echo Please ensure:
    echo 1. WSL is installed
    echo 2. The vibe-coder folder exists
    echo 3. Run setup first: ./setup.sh
    echo.
    pause
)
