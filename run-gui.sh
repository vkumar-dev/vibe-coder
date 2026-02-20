#!/bin/bash
# Vibe Coder GUI Launcher for Linux/Mac
# Double-click this file to open the GUI

TITLE="Vibe Coder - Autonomous App Factory"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "  Vibe Coder - Starting GUI..."
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found!"
    echo "Please install Python 3.8+"
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "venv/bin/python" ]; then
    echo "Virtual environment not found!"
    echo "Running setup..."
    bash setup.sh
    if [ $? -ne 0 ]; then
        echo "Setup failed!"
        exit 1
    fi
fi

# Activate virtual environment and run GUI
echo "Starting GUI..."
source venv/bin/activate
python3 gui.py

# If GUI exits, show message
echo ""
echo "GUI closed."
