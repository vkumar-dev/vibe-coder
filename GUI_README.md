# Vibe Coder GUI - Desktop Application

## 🎨 Quick Start

### Windows
**Double-click:** `run-gui.bat`

*(First time only: Run `setup.bat` first)*

### Linux/Mac
**Double-click:** `run-gui.sh`

Or run from terminal:
```bash
./run-gui.sh
```

---

## Features

### Main Window
- **Live Progress Log** - See real-time output from Vibe Coder
- **Status Display** - Apps generated, last cycle time, running state
- **Start/Stop Controls** - One-click control of Vibe Coder
- **Mode Selection** - Single run or continuous daemon mode
- **Interval Setting** - Customize how often to generate apps (1-24 hours)

### Quick Actions
- **Open Projects Folder** - View all generated apps
- **View Status** - Detailed status report
- **List Apps** - See all generated apps

### Background Operation
- GUI can be minimized while Vibe Coder runs in background
- Stop button kills the background process
- Auto-cleanup on window close

---

## Screenshots

### Main Interface
```
┌────────────────────────────────────────────────┐
│         🎨 Vibe Coder                          │
│   Ship 6 products per day while you sleep      │
├────────────────────────────────────────────────┤
│ Status:                                        │
│ State: Running 🟢                              │
│ Apps Generated: 2                              │
│ Last Cycle: 2026-02-20T17:00:00               │
├────────────────────────────────────────────────┤
│ Controls:                                      │
│ Mode: ○ Single Run  ● Continuous (Daemon)     │
│ Interval: [4] hours                            │
│ [▶ Start] [⏹ Stop] [🔄 Refresh]               │
├────────────────────────────────────────────────┤
│ Live Log:                                      │
│ [17:00:01] Starting daemon mode...            │
│ [17:00:02] Researching GitHub trending...     │
│ [17:00:05] Generating app ideas...            │
│ [17:00:10] ✨ App generated!                  │
│ [17:00:11] Next cycle in 4 hours              │
├────────────────────────────────────────────────┤
│ [📂 Open Projects] [📊 View Status] [📋 List] │
└────────────────────────────────────────────────┘
```

---

## Installation

### First Time Setup (Windows)
1. Double-click `setup.bat`
2. Wait for installation to complete
3. Double-click `run-gui.bat`

### First Time Setup (Linux/Mac)
```bash
chmod +x run-gui.sh setup.sh
./setup.sh
./run-gui.sh
```

---

## Usage

### Mode 1: Single Run
- Select "Single Run" radio button
- Click "▶ Start"
- Generates 1 app and stops
- Good for testing

### Mode 2: Continuous (Daemon)
- Select "Continuous (Daemon)" radio button
- Set interval (default: 4 hours)
- Click "▶ Start"
- Generates 1 app every X hours
- Runs until you click "⏹ Stop"

### Stopping Vibe Coder
1. Click "⏹ Stop" button
2. Confirm when prompted
3. Background process terminates

### Closing GUI
- If Vibe Coder is running, you'll be asked to confirm
- Choose to stop and exit, or keep running in background

---

## Files

| File | Purpose |
|------|---------|
| `gui.py` | Main GUI application |
| `run-gui.bat` | Windows launcher |
| `run-gui.sh` | Linux/Mac launcher |
| `setup.bat` | Windows setup script |
| `setup.sh` | Linux/Mac setup script |

---

## Troubleshooting

### "Python not found"
Install Python 3.8+ from https://python.org

### "Virtual environment not found"
Run `setup.bat` (Windows) or `./setup.sh` (Linux/Mac)

### GUI won't open
Try running from terminal:
```bash
python gui.py
```

### Can't stop Vibe Coder
Close the GUI window and run:
```bash
pkill -f vibe_coder.py  # Linux/Mac
taskkill /F /IM python.exe  # Windows (kills all Python)
```

---

## System Requirements

- **OS:** Windows 10+, macOS 10.14+, Linux (any modern distro)
- **Python:** 3.8+
- **RAM:** 512MB minimum
- **Disk:** 1GB free space

---

## Tips

1. **Minimize, don't close** - Keep GUI minimized while Vibe Coder runs
2. **Check logs** - Live log shows what's happening
3. **Start with single run** - Test with single run before daemon mode
4. **Monitor first few cycles** - Make sure everything works as expected

---

## Keyboard Shortcuts

- **Ctrl+R** - Refresh status
- **Ctrl+S** - Start/Stop toggle
- **Esc** - Close GUI (prompts to stop if running)

---

**Happy vibe coding! 🎨**
