#!/bin/bash

################################################################################
# Vibe Coder - Quick Start
#
# One command to start the vibe coder daemon.
#
# Usage: ./quickstart.sh
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "========================================"
echo "  🎨 Vibe Coder - Quick Start"
echo "========================================"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 First time setup detected..."
    echo "   Running setup..."
    bash setup.sh
fi

# Activate venv
source venv/bin/activate

# Check if already running
if [ -f ".vibe-loop/worker.pid" ]; then
    WORKER_PID=$(cat .vibe-loop/worker.pid)
    if kill -0 "$WORKER_PID" 2>/dev/null; then
        echo "⚠️  Vibe Coder is already running (PID: $WORKER_PID)"
        echo ""
        echo "Options:"
        echo "  Stop:  kill $WORKER_PID"
        echo "  Logs:  tail -f .vibe-loop/worker.output"
        echo "  Status: python vibe_coder.py status"
        exit 0
    fi
fi

# Start daemon
echo "🚀 Starting Vibe Coder daemon..."
echo "   Generating 1 app every 4 hours"
echo "   Press Ctrl+C to stop"
echo ""

python vibe_coder.py daemon --interval 4
