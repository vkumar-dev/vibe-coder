#!/bin/bash

################################################################################
# Vibe Coder - One Liner Setup
#
# Usage: curl -sSL https://github.com/vkumar-dev/vibe-coder/raw/main/install.sh | bash
#    or: wget -qO- https://github.com/vkumar-dev/vibe-coder/raw/main/install.sh | bash
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
INSTALL_DIR="${INSTALL_DIR:-$HOME/vibe-coder}"
GITHUB_REPO="vkumar-dev/vibe-coder"
BRANCH="${BRANCH:-main}"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   🎨 Vibe Coder - One Liner Install   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Check prerequisites
echo -e "${YELLOW}📦 Checking prerequisites...${NC}"

# Check git
if ! command -v git &> /dev/null; then
    echo -e "${RED}❌ git not found. Please install git first.${NC}"
    echo "   Ubuntu/Debian: sudo apt install git"
    echo "   macOS: xcode-select --install"
    exit 1
fi
echo -e "${GREEN}✓${NC} git found"

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    echo "   Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "   macOS: brew install python3"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} $PYTHON_VERSION"

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}⚠️  pip3 not found, trying to continue...${NC}"
fi

# Check gh CLI (optional)
if command -v gh &> /dev/null; then
    echo -e "${GREEN}✓${NC} gh CLI found (GitHub integration enabled)"
    GH_AVAILABLE=true
else
    echo -e "${YELLOW}⚠️  gh CLI not found (GitHub features limited)${NC}"
    echo -e "${YELLOW}   Install: ${BLUE}https://cli.github.com/${NC}"
    GH_AVAILABLE=false
fi

# Clone repository
echo ""
echo -e "${YELLOW}📦 Cloning vibe-coder...${NC}"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Directory exists: $INSTALL_DIR${NC}"
    echo -n "Remove and reinstall? [y/N] "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        rm -rf "$INSTALL_DIR"
        echo "Removed old installation"
    else
        echo -e "${YELLOW}Using existing installation${NC}"
    fi
fi

if [ ! -d "$INSTALL_DIR" ]; then
    git clone --depth 1 "https://github.com/$GITHUB_REPO.git" "$INSTALL_DIR"
    echo -e "${GREEN}✓${NC} Cloned to $INSTALL_DIR"
fi

cd "$INSTALL_DIR"

# Create virtual environment
echo ""
echo -e "${YELLOW}📦 Creating virtual environment...${NC}"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment exists"
fi

# Activate and install dependencies
echo ""
echo -e "${YELLOW}📦 Installing dependencies...${NC}"

source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo -e "${GREEN}✓${NC} Dependencies installed"

# Make scripts executable
chmod +x *.sh 2>/dev/null || true

# Create directories
mkdir -p projects logs state

# Setup .env if not exists
if [ ! -f ".env" ]; then
    cat > .env << 'EOF'
# Vibe Coder Configuration

# GitHub username (for auto-push)
GITHUB_USER=vkumar-dev

# Optional: AI API Keys (get free credits)
# Anthropic: https://console.anthropic.com
# OpenAI: https://platform.openai.com
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# Optional: Notifications
# SLACK_WEBHOOK=
# DISCORD_WEBHOOK=
EOF
    echo -e "${GREEN}✓${NC} Created .env template"
fi

# Check GitHub auth
if [ "$GH_AVAILABLE" = true ]; then
    echo ""
    echo -e "${YELLOW}📦 Checking GitHub authentication...${NC}"
    if gh auth status &> /dev/null; then
        echo -e "${GREEN}✓${NC} GitHub authenticated"
    else
        echo -e "${YELLOW}⚠️  Not authenticated with GitHub${NC}"
        echo -e "${YELLOW}   Run: ${BLUE}gh auth login${NC}"
        echo -e "${YELLOW}   (Required for auto-push to GitHub)${NC}"
    fi
fi

# Show completion message
echo ""
echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        ✅ Setup Complete!              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}Installation directory:${NC} $INSTALL_DIR"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo ""
echo "1. Activate environment:"
echo -e "   ${BLUE}cd $INSTALL_DIR && source venv/bin/activate${NC}"
echo ""
echo "2. (Optional) Authenticate with GitHub:"
echo -e "   ${BLUE}gh auth login${NC}"
echo ""
echo "3. Run your first cycle:"
echo -e "   ${BLUE}python vibe_coder.py run${NC}"
echo ""
echo "4. Run continuously (1 app every 4 hours):"
echo -e "   ${BLUE}python vibe_coder.py daemon${NC}"
echo ""
echo "5. Or use Ralph Loop (resilient):"
echo -e "   ${BLUE}./supervisor.sh${NC}"
echo ""
echo -e "${YELLOW}Quick reference:${NC}"
echo -e "   ${BLUE}python vibe_coder.py status${NC}  - Check status"
echo -e "   ${BLUE}python vibe_coder.py list${NC}    - List generated apps"
echo -e "   ${BLUE}tail -f logs/vibe-coder.log${NC}  - View logs"
echo ""
echo -e "${BLUE}🎨 Happy vibe coding!${NC}"
echo ""
