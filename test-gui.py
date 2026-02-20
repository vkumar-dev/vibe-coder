#!/usr/bin/env python3
"""
Vibe Coder GUI - Test Launch

Quick test to verify GUI can start.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import tkinter as tk
    print("✓ Tkinter imported successfully")
    
    # Try to create a window
    root = tk.Tk()
    root.title("Vibe Coder GUI Test")
    root.geometry("400x300")
    
    label = tk.Label(root, text="🎨 Vibe Coder GUI\n\nTest Successful!\n\nClose this window to exit.", 
                     font=('Helvetica', 16), justify='center')
    label.pack(expand=True)
    
    print("✓ GUI window created")
    print("✓ GUI is working correctly!")
    print("\nYou can now run: python gui.py")
    
    root.mainloop()
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Make sure tkinter is installed:")
    print("   Ubuntu: sudo apt install python3-tk")
    print("   Fedora: sudo dnf install python3-tkinter")
    print("   Windows: tkinter comes with Python")
    print("   Mac: tkinter comes with Python")
    sys.exit(1)
