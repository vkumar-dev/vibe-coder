#!/bin/bash
# Create Desktop Shortcut for Vibe Coder GUI (macOS)

echo "========================================"
echo "  Creating Desktop Shortcut..."
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Desktop path
DESKTOP_DIR="$HOME/Desktop"

# Create AppleScript application
cat > "$DESKTOP_DIR/Vibe Coder.app/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Vibe Coder</string>
    <key>CFBundleIdentifier</key>
    <string>com.vibecoder.app</string>
    <key>CFBundleName</key>
    <string>Vibe Coder</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
</dict>
</plist>
EOF

# Create launcher script
mkdir -p "$DESKTOP_DIR/Vibe Coder.app/Contents/MacOS"
cat > "$DESKTOP_DIR/Vibe Coder.app/Contents/MacOS/Vibe Coder" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"
./run-gui.sh
EOF

chmod +x "$DESKTOP_DIR/Vibe Coder.app/Contents/MacOS/Vibe Coder"

echo "✅ Desktop shortcut created!"
echo ""
echo "   Location: $DESKTOP_DIR/Vibe Coder.app"
echo ""
echo "   You can now double-click the app to start Vibe Coder!"
echo ""
