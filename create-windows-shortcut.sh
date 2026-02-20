#!/bin/bash
# Create Windows Desktop Shortcut for Vibe Coder GUI (WSL)
# Detects Windows desktop path and creates .lnk shortcut

set -e

echo "========================================"
echo "  Creating Windows Desktop Shortcut"
echo "  (WSL Environment)"
echo "========================================"
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get Windows Desktop path via PowerShell
echo "📍 Detecting Windows Desktop path..."
WIN_DESKTOP=$(powershell.exe -c "[Environment]::GetFolderPath('Desktop')" 2>/dev/null | tr -d '\r\n' | sed 's/\\/\//g' | sed 's/^C:/\/mnt\/c/')

if [ -z "$WIN_DESKTOP" ]; then
    # Fallback paths
    if [ -d "/mnt/c/Users/vijay/OneDrive/Desktop" ]; then
        WIN_DESKTOP="/mnt/c/Users/vijay/OneDrive/Desktop"
    elif [ -d "/mnt/c/Users/vijay/Desktop" ]; then
        WIN_DESKTOP="/mnt/c/Users/vijay/Desktop"
    elif [ -d "/mnt/c/Users/Public/Desktop" ]; then
        WIN_DESKTOP="/mnt/c/Users/Public/Desktop"
    else
        echo "❌ Could not find Windows Desktop path"
        echo ""
        echo "Please manually create shortcut to:"
        echo "  $SCRIPT_DIR/run-gui.sh"
        exit 1
    fi
fi

echo "✅ Windows Desktop: $WIN_DESKTOP"
echo ""

# Convert to Windows path for display
WIN_PATH_DISPLAY=$(echo "$WIN_DESKTOP" | sed 's/\/mnt\/[a-z]\//\//g' | sed 's/\//\\/g')
WIN_PATH_DISPLAY="C:${WIN_PATH_DISPLAY}"

# Create VBScript for creating .lnk file
VBS_FILE="/tmp/create_shortcut.vbs"
cat > "$VBS_FILE" << EOF
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

strScriptDir = "$SCRIPT_DIR"
strDesktop = "$WIN_DESKTOP"
strTarget = strScriptDir & "\\run-gui.sh"
strShortcut = strDesktop & "\\Vibe Coder.lnk"

Set oShellLink = WshShell.CreateShortcut(strShortcut)
oShellLink.TargetPath = "C:\\Windows\\System32\\wsl.exe"
oShellLink.Arguments = "--cd " & strScriptDir & " -e bash -c " & chr(34) & "./run-gui.sh" & chr(34)
oShellLink.WorkingDirectory = strScriptDir
oShellLink.Description = "Vibe Coder - Autonomous App Factory"
oShellLink.IconLocation = "C:\\Windows\\System32\\wsl.exe,0"
oShellLink.Save

WScript.Echo "Shortcut created: " & strShortcut
EOF

# Run VBScript via Windows cscript
echo "🔧 Creating Windows shortcut..."
if powershell.exe -c "cscript.exe //nologo $VBS_FILE" 2>&1; then
    echo ""
    echo "========================================"
    echo "  ✅ Windows Desktop Shortcut Created!"
    echo "========================================"
    echo ""
    echo "📍 Location: $WIN_DESKTOP/Vibe Coder.lnk"
    echo ""
    echo "   You can now double-click the shortcut"
    echo "   on your Windows Desktop to start!"
    echo ""
else
    echo "❌ Failed to create shortcut via PowerShell"
    echo ""
    echo "Creating manual shortcut file..."
    
    # Create a better batch file on Windows desktop instead
    BAT_FILE="$WIN_DESKTOP/Vibe Coder.bat"
    cat > "$BAT_FILE" << 'EOF'
@echo off
REM Vibe Coder - Autonomous App Factory
title Vibe Coder
echo ========================================
echo   Vibe Coder - Starting...
echo ========================================
echo.
wsl --cd "/home/eliza/qwen/vibe-coder" -e bash -c "./run-gui.sh"
if %errorlevel% neq 0 (
    echo.
    echo Error: Please run setup first
    echo Run: wsl -e bash -c "cd /home/eliza/qwen/vibe-coder && ./setup.sh"
    echo.
    pause
)
EOF
    
    if [ -f "$BAT_FILE" ]; then
        echo "✅ Created batch launcher instead"
        echo ""
        echo "📍 Location: $BAT_FILE"
        echo ""
        echo "   Double-click 'Vibe Coder.bat' on your"
        echo "   Windows Desktop to start!"
        echo ""
    else
        echo "❌ Could not create shortcut"
        echo ""
        echo "Manual steps:"
        echo "1. Open Windows Explorer"
        echo "2. Navigate to: $WIN_PATH_DISPLAY"
        echo "3. Create shortcut to: wsl.exe"
        echo "4. Set arguments: --cd $SCRIPT_DIR -e bash ./run-gui.sh"
        exit 1
    fi
fi

# Cleanup
rm -f "$VBS_FILE"

echo "🎨 Happy vibe coding!"
echo ""
