# 🎨 Vibe Coder GUI - Complete Guide

## ✅ What Was Created

A full-featured **desktop GUI application** for Vibe Coder that you can **double-click to open**!

---

## 🚀 Quick Start

### Windows
1. **First time:** Double-click `setup.bat`
2. **Run GUI:** Double-click `run-gui.bat`

### Linux/Mac
1. **First time:** Run `./setup.sh`
2. **Run GUI:** Double-click `run-gui.sh` or run `./run-gui.sh`

---

## 📸 GUI Features

### Main Window
```
┌────────────────────────────────────────────────────┐
│           🎨 Vibe Coder                            │
│      Ship 6 products per day while you sleep       │
├────────────────────────────────────────────────────┤
│  Status:                                           │
│  ├─ State: Running 🟢                             │
│  ├─ Apps Generated: 2                             │
│  └─ Last Cycle: 2026-02-20T17:00:00              │
├────────────────────────────────────────────────────┤
│  Controls:                                         │
│  ├─ Mode: ○ Single Run  ● Continuous              │
│  ├─ Interval: [4] hours  (1-24)                   │
│  └─ [▶ Start] [⏹ Stop] [🔄 Refresh]              │
├────────────────────────────────────────────────────┤
│  Live Log:                                         │
│  ├─ [17:00:01] Starting daemon mode...            │
│  ├─ [17:00:05] Researching GitHub trending...     │
│  ├─ [17:00:10] ✨ App generated!                  │
│  └─ [17:00:15] Next cycle in 4 hours              │
├────────────────────────────────────────────────────┤
│  [📂 Open Projects] [📊 View Status] [📋 List]    │
└────────────────────────────────────────────────────┘
```

### Features Breakdown

| Feature | Description |
|---------|-------------|
| **Live Log** | Real-time output from Vibe Coder |
| **Status Display** | Apps generated, last cycle time, running state |
| **Start Button** | Start Vibe Coder with selected mode |
| **Stop Button** | Stop the background process |
| **Mode Selection** | Single run or continuous daemon |
| **Interval Control** | Set hours between app generation (1-24) |
| **Open Projects** | Open projects folder in file manager |
| **View Status** | Show detailed status report |
| **List Apps** | Display all generated apps |
| **Progress Bar** | Visual indicator when running |

---

## 📁 Files Created

| File | Purpose | Platform |
|------|---------|----------|
| `gui.py` | Main GUI application | All |
| `run-gui.bat` | Windows launcher | Windows |
| `run-gui.sh` | Linux/Mac launcher | Linux/Mac |
| `setup.bat` | Windows setup | Windows |
| `setup.sh` | Linux/Mac setup | Linux/Mac |
| `test-gui.py` | GUI test script | All |
| `GUI_README.md` | GUI documentation | All |

---

## 🎯 How to Use

### Mode 1: Single Run (Test)
1. Select **"Single Run"** radio button
2. Click **"▶ Start"**
3. Watch the live log
4. Generates 1 app and stops

### Mode 2: Continuous (Production)
1. Select **"Continuous (Daemon)"** radio button
2. Set interval (default: 4 hours)
3. Click **"▶ Start"**
4. Generates 1 app every X hours
5. Minimize GUI (keeps running in background)
6. Click **"⏹ Stop"** when you want to stop

### Stopping Vibe Coder
1. Click **"⏹ Stop"** button
2. Confirm when prompted
3. Background process terminates gracefully

### Closing GUI
- If running, you'll be asked: "Stop and exit?"
- **Yes** - Stops Vibe Coder and closes
- **No** - Minimizes to background (keeps running)

---

## 🔧 Installation

### Windows (First Time)
```
1. Double-click setup.bat
2. Wait for installation (2-3 minutes)
3. Double-click run-gui.bat
4. GUI opens!
```

### Linux/Mac (First Time)
```bash
chmod +x run-gui.sh setup.sh
./setup.sh
./run-gui.sh
```

### Test GUI (Optional)
```bash
python test-gui.py
```

Should show: "✓ GUI is working correctly!"

---

## 💡 Tips & Tricks

### 1. Minimize, Don't Close
- Minimize GUI while Vibe Coder runs
- Check back periodically to see progress

### 2. Start with Single Run
- Test with "Single Run" first
- Verify everything works
- Then switch to "Continuous"

### 3. Monitor First Few Cycles
- Watch the live log
- Make sure apps are generating
- Check for any errors

### 4. Use Quick Actions
- **Open Projects** - See generated apps
- **View Status** - Detailed statistics
- **List Apps** - All apps with paths

### 5. Background Operation
- GUI can be minimized
- Vibe Coder runs independently
- Stop anytime with Stop button

---

## 🐛 Troubleshooting

### "Python not found"
**Windows:** Install from https://python.org  
**Linux:** `sudo apt install python3 python3-venv python3-pip`  
**Mac:** `brew install python3`

### "Tkinter not available"
**Windows:** Comes with Python  
**Linux:** `sudo apt install python3-tk`  
**Mac:** Comes with Python

### "Virtual environment not found"
Run `setup.bat` (Windows) or `./setup.sh` (Linux/Mac)

### GUI won't start
Try from terminal:
```bash
python gui.py
```

Check error message for clues.

### Can't stop Vibe Coder
**Linux/Mac:**
```bash
pkill -f vibe_coder.py
```

**Windows:**
```bash
taskkill /F /IM python.exe
```

### Live log not updating
- Click "Refresh" button
- Check if process is still running
- Restart if needed

---

## 📊 What Happens When You Click Start

1. **Validates** - Checks mode and interval
2. **Spawns Process** - Starts `vibe_coder.py` as subprocess
3. **Reads Output** - Captures stdout/stderr in real-time
4. **Updates Log** - Appends lines to live log with colors
5. **Monitors** - Watches for process end
6. **Updates Status** - Refreshes stats every 5 seconds

---

## 🎨 Color Coding in Log

| Color | Meaning | Example |
|-------|---------|---------|
| **Blue** | Info | "Starting daemon mode..." |
| **Green** | Success | "✨ App generated!" |
| **Orange** | Warning | "⚠️ qwen-code not found" |
| **Red** | Error | "❌ Failed to start" |

---

## ⚙️ System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Windows 10, macOS 10.14, Linux | Latest |
| **Python** | 3.8 | 3.10+ |
| **RAM** | 512 MB | 1 GB |
| **Disk** | 1 GB | 5 GB+ |
| **Display** | 800x600 | 1024x768+ |

---

## 📈 Example Session

```
[17:00:00] User clicks "Start" (Continuous, 4h)
[17:00:01] Starting daemon mode (interval: 4h)...
[17:00:02] Vibe Coder started successfully!
[17:00:03] 🔍 Researching GitHub trending...
[17:00:05] 🔍 Researching Hacker News...
[17:00:07] 💡 Generating app ideas from 10 trends...
[17:00:08] 📋 Processing idea: AI-Powered: Some Topic
[17:00:09] 🔍 Checking duplicates...
[17:00:10] ✅ No duplicates found
[17:00:11] 🚀 Generating app...
[17:00:15] ✨ App generated successfully in 4.2s
[17:00:16] 📦 Repo: vkumar-dev/vibe-ai-powered-some-topic
[17:00:17] 💤 Next cycle in 4 hours
```

User minimizes GUI...

*(4 hours later)*

```
[21:00:00] 🚀 Running next cycle...
[21:00:05] ✨ App generated successfully!
```

User clicks "Stop"...

```
[21:05:00] User clicks "Stop"
[21:05:01] Vibe Coder stopped
[21:05:02] Process ended
```

---

## 🎓 Advanced Usage

### Run Without GUI (Terminal)
```bash
# Single run
python vibe_coder.py run

# Continuous
python vibe_coder.py daemon --interval 4

# Ralph Loop (auto-restart)
./supervisor.sh
```

### Custom Interval
Change interval in GUI or use:
```bash
python vibe_coder.py daemon --interval 6  # Every 6 hours
```

### View Logs Manually
```bash
# Live tail
tail -f logs/vibe-coder.log

# Generation history
cat state/history.json | jq
```

---

## 📞 Support

- **GUI Issues:** Check `GUI_README.md`
- **Vibe Coder Issues:** Check `README.md`
- **Deployment:** Check `DEPLOY.md`
- **GitHub:** https://github.com/vkumar-dev/vibe-coder

---

## 🎉 Summary

You now have a **full-featured desktop GUI** for Vibe Coder:

✅ **Double-click to run** (no terminal needed)  
✅ **Live progress monitoring**  
✅ **Start/Stop controls**  
✅ **Background operation**  
✅ **Quick access to projects**  
✅ **Cross-platform** (Windows, Linux, Mac)  

**Just double-click `run-gui.bat` (Windows) or `run-gui.sh` (Linux/Mac) and start generating apps!**

---

**Happy vibe coding! 🎨**
