#!/bin/bash
# Create Desktop Shortcut for Vibe Coder GUI (Linux)

echo "========================================"
echo "  Creating Desktop Shortcut..."
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect desktop environment
if [ -d "$HOME/Desktop" ]; then
    DESKTOP_DIR="$HOME/Desktop"
elif [ -d "$HOME/Bureau" ]; then
    DESKTOP_DIR="$HOME/Bureau"
else
    DESKTOP_DIR="$HOME/Desktop"
    mkdir -p "$DESKTOP_DIR"
fi

# Create .desktop file
cat > "$DESKTOP_DIR/vibe-coder.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Vibe Coder
Comment=Autonomous App Factory - Ship 6 products per day
Exec=bash -c "cd '$SCRIPT_DIR' && ./run-gui.sh"
Path=$SCRIPT_DIR
Icon=utilities-terminal
Terminal=false
Categories=Development;Utility;
EOF

# Make executable
chmod +x "$DESKTOP_DIR/vibe-coder.desktop"

echo "✅ Desktop shortcut created!"
echo ""
echo "   Location: $DESKTOP_DIR/vibe-coder.desktop"
echo ""
echo "   You can now double-click the shortcut to start Vibe Coder!"
echo ""

# Try to set as trusted (for GNOME)
if command -v gio &> /dev/null; then
    gio set "$DESKTOP_DIR/vibe-coder.desktop" metadata::trusted true 2>/dev/null || true
fi
