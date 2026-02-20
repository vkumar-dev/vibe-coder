#!/bin/bash

################################################################################
# Vibe Coder - Setup Script
#
# Installs dependencies and configures the vibe coder system.
#
# Usage: ./setup.sh
################################################################################

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo ""
echo "========================================"
echo "  🎨 Vibe Coder - Setup"
echo "========================================"
echo ""

# Check Python
echo "📦 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION"
else
    echo "❌ Python 3 not found"
    echo "   Please install Python 3.8+"
    exit 1
fi

# Check pip
echo "📦 Checking pip..."
if command -v pip3 &> /dev/null; then
    echo "✅ pip3 found"
else
    echo "❌ pip3 not found"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
else
    echo "⚠️  No requirements.txt found"
fi

# Check gh CLI
echo ""
echo "📦 Checking GitHub CLI..."
if command -v gh &> /dev/null; then
    GH_VERSION=$(gh --version | head -1)
    echo "✅ $GH_VERSION"
else
    echo "⚠️  gh CLI not found"
    echo "   Install from: https://cli.github.com/"
    echo "   Required for: GitHub repo checks, auto-push"
fi

# Check qwen-code CLI
echo ""
echo "📦 Checking qwen-code CLI..."
if command -v qwen-code &> /dev/null; then
    echo "✅ qwen-code found"
else
    echo "⚠️  qwen-code CLI not found"
    echo "   The system will use template generation instead"
    echo "   Install qwen-code for full AI-powered generation"
fi

# Create directories
echo ""
echo "📦 Creating directories..."
mkdir -p projects logs state

# Make scripts executable
echo "📦 Making scripts executable..."
chmod +x worker.sh supervisor.sh vibe_coder.py

# Initialize git (if not already)
echo ""
echo "📦 Checking git..."
if [ ! -d ".git" ]; then
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git already initialized"
fi

# Check GitHub auth
echo ""
echo "📦 Checking GitHub authentication..."
if command -v gh &> /dev/null; then
    if gh auth status &> /dev/null; then
        echo "✅ GitHub authenticated"
    else
        echo "⚠️  Not authenticated with GitHub"
        echo "   Run: gh auth login"
    fi
fi

# Create .env file if not exists
if [ ! -f ".env" ]; then
    echo ""
    echo "📦 Creating .env template..."
    cat > .env << 'EOF'
# Vibe Coder Configuration

# GitHub username for repo creation
GITHUB_USER=vkumar-dev

# Optional: API keys for enhanced features
# OPENAI_API_KEY=
# ANTHROPIC_API_KEY=

# Notification settings (optional)
# SLACK_WEBHOOK=
# DISCORD_WEBHOOK=
EOF
    echo "✅ .env created"
else
    echo "✅ .env already exists"
fi

# Show next steps
echo ""
echo "========================================"
echo "  ✅ Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. (Optional) Authenticate with GitHub:"
echo "   gh auth login"
echo ""
echo "3. Run a single cycle:"
echo "   python vibe_coder.py run"
echo ""
echo "4. Run continuously (1 app every 4 hours):"
echo "   python vibe_coder.py daemon"
echo ""
echo "5. Or use Ralph Loop supervisor:"
echo "   ./supervisor.sh"
echo ""
echo "========================================"
echo ""
