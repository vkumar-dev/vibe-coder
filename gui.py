#!/usr/bin/env python3
"""
Vibe Coder - GUI Application

A desktop GUI for controlling the Vibe Coder autonomous app factory.
Double-click to run!
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import threading
import os
import sys
import signal
import json
from datetime import datetime
from pathlib import Path


class VibeCoderGUI:
    """Main GUI Application"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Vibe Coder - Autonomous App Factory")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Set icon (emoji as fallback)
        try:
            self.root.iconbitmap(default='')
        except:
            pass
        
        # Variables
        self.process = None
        self.is_running = False
        self.mode = tk.StringVar(value="daemon")
        self.interval = tk.StringVar(value="4")
        self.app_dir = Path(__file__).parent.absolute()
        self.venv_python = self.app_dir / "venv" / "bin" / "python"
        
        # Check if venv exists
        if not self.venv_python.exists():
            self.venv_python = sys.executable
        
        # Setup UI
        self.setup_styles()
        self.create_widgets()
        self.load_status()
        
        # Start status update loop
        self.update_status()
    
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        
        # Try to use a modern theme
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Configure colors
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'), foreground='#667eea')
        style.configure('Status.TLabel', font=('Helvetica', 12), foreground='#2ecc71')
        style.configure('Error.TLabel', font=('Helvetica', 12), foreground='#e74c3c')
        style.configure('Big.TButton', font=('Helvetica', 12, 'bold'), padding=10)
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🎨 Vibe Coder",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 5))
        
        subtitle_label = ttk.Label(
            main_frame,
            text="Ship 6 products per day while you sleep"
        )
        subtitle_label.grid(row=1, column=0, pady=(0, 20))
        
        # Status Frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        status_frame.columnconfigure(1, weight=1)
        
        ttk.Label(status_frame, text="State:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(status_frame, text="Stopped", style='Status.TLabel')
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Label(status_frame, text="Apps Generated:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.apps_label = ttk.Label(status_frame, text="0")
        self.apps_label.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        ttk.Label(status_frame, text="Last Cycle:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.last_cycle_label = ttk.Label(status_frame, text="Never")
        self.last_cycle_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Control Frame
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        control_frame.columnconfigure(2, weight=1)
        
        # Mode selection
        ttk.Label(control_frame, text="Mode:").grid(row=0, column=0, sticky=tk.W)
        
        mode_frame = ttk.Frame(control_frame)
        mode_frame.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        ttk.Radiobutton(
            mode_frame,
            text="Single Run",
            variable=self.mode,
            value="run"
        ).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Radiobutton(
            mode_frame,
            text="Continuous (Daemon)",
            variable=self.mode,
            value="daemon"
        ).grid(row=0, column=1, padx=(0, 10))
        
        # Interval (only for daemon)
        ttk.Label(control_frame, text="Interval (hours):").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.interval_spinbox = ttk.Spinbox(
            control_frame,
            from_=1,
            to=24,
            width=5,
            textvariable=self.interval
        )
        self.interval_spinbox.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))
        
        # Buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=0, column=2, rowspan=2, sticky=tk.E)
        
        self.start_button = ttk.Button(
            button_frame,
            text="▶ Start",
            command=self.start_vibe_coder,
            style='Big.TButton'
        )
        self.start_button.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_button = ttk.Button(
            button_frame,
            text="⏹ Stop",
            command=self.stop_vibe_coder,
            state=tk.DISABLED,
            style='Big.TButton'
        )
        self.stop_button.grid(row=0, column=1, padx=(0, 5))
        
        self.refresh_button = ttk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self.load_status
        )
        self.refresh_button.grid(row=0, column=2)
        
        # Log Output
        log_frame = ttk.LabelFrame(main_frame, text="Live Log", padding="10")
        log_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=('Courier', 9)
        )
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure text tags for colors
        self.log_text.tag_configure('info', foreground='#2980b9')
        self.log_text.tag_configure('success', foreground='#27ae60')
        self.log_text.tag_configure('warning', foreground='#f39c12')
        self.log_text.tag_configure('error', foreground='#c0392b')
        
        # Quick Actions
        actions_frame = ttk.Frame(main_frame)
        actions_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        
        ttk.Button(
            actions_frame,
            text="📂 Open Projects Folder",
            command=self.open_projects_folder
        ).grid(row=0, column=0, padx=(0, 5))
        
        ttk.Button(
            actions_frame,
            text="📊 View Status",
            command=self.view_full_status
        ).grid(row=0, column=1, padx=(0, 5))
        
        ttk.Button(
            actions_frame,
            text="📋 List Apps",
            command=self.list_apps
        ).grid(row=0, column=2)
        
        # Progress Bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=6, column=0, pady=(0, 10))
    
    def log(self, message, level='info'):
        """Add message to log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", level)
        self.log_text.see(tk.END)
    
    def start_vibe_coder(self):
        """Start Vibe Coder process"""
        if self.is_running:
            messagebox.showwarning("Already Running", "Vibe Coder is already running!")
            return
        
        mode = self.mode.get()
        interval = self.interval.get()
        
        # Build command
        cmd = [str(self.venv_python), str(self.app_dir / "vibe_coder.py")]
        
        if mode == "run":
            cmd.extend(["run"])
            self.log("Starting single run...", 'info')
        else:
            cmd.extend(["daemon", "--interval", interval])
            self.log(f"Starting daemon mode (interval: {interval}h)...", 'info')
        
        try:
            # Start process
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=str(self.app_dir),
                bufsize=1,
                universal_newlines=True
            )
            
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.progress.start()
            self.status_label.config(text="Running", style='Status.TLabel')
            
            # Start output reader thread
            thread = threading.Thread(target=self.read_output, daemon=True)
            thread.start()
            
            self.log("Vibe Coder started successfully!", 'success')
            
        except Exception as e:
            self.log(f"Failed to start: {e}", 'error')
            messagebox.showerror("Error", f"Failed to start Vibe Coder:\n{e}")
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
    
    def read_output(self):
        """Read process output in background thread"""
        try:
            for line in self.process.stdout:
                if line.strip():
                    # Schedule GUI update
                    self.root.after(0, self.append_log, line.strip())
                
                # Check for specific patterns
                if "App generated successfully" in line:
                    self.root.after(0, lambda: self.log("✨ App generated!", 'success'))
                elif "ERROR" in line or "failed" in line.lower():
                    self.root.after(0, lambda: self.log(line.strip(), 'error'))
                elif "⚠" in line or "Warning" in line:
                    self.root.after(0, lambda: self.log(line.strip(), 'warning'))
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Output reader error: {e}", 'error'))
        finally:
            self.root.after(0, self.process_ended)
    
    def append_log(self, line):
        """Append line to log (called from main thread)"""
        self.log_text.insert(tk.END, line + "\n", 'info')
        self.log_text.see(tk.END)
    
    def process_ended(self):
        """Called when process ends"""
        self.is_running = False
        self.process = None
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress.stop()
        self.status_label.config(text="Stopped", style='Status.TLabel')
        self.log("Process ended", 'info')
        self.load_status()
    
    def stop_vibe_coder(self):
        """Stop Vibe Coder process"""
        if not self.is_running or not self.process:
            return
        
        if messagebox.askyesno("Confirm Stop", "Are you sure you want to stop Vibe Coder?"):
            try:
                # Try graceful shutdown
                self.process.terminate()
                
                # Wait a bit
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    self.process.kill()
                    self.process.wait()
                
                self.log("Vibe Coder stopped", 'warning')
                
            except Exception as e:
                self.log(f"Error stopping: {e}", 'error')
            finally:
                self.process_ended()
    
    def load_status(self):
        """Load current status from state file"""
        try:
            state_file = self.app_dir / "state" / "history.json"
            if state_file.exists():
                with open(state_file, 'r') as f:
                    history = json.load(f)
                
                if history:
                    total_apps = sum(h.get('apps_generated', 0) for h in history)
                    last_cycle = history[-1].get('cycle_end', 'Unknown')
                    
                    self.apps_label.config(text=str(total_apps))
                    self.last_cycle_label.config(text=last_cycle[:19] if len(last_cycle) > 19 else last_cycle)
        except Exception as e:
            self.log(f"Error loading status: {e}", 'error')
    
    def update_status(self):
        """Periodically update status"""
        self.load_status()
        self.root.after(5000, self.update_status)  # Update every 5 seconds
    
    def open_projects_folder(self):
        """Open projects folder in file manager"""
        projects_dir = self.app_dir / "projects"
        if projects_dir.exists():
            try:
                if sys.platform == 'win32':
                    os.startfile(str(projects_dir))
                elif sys.platform == 'darwin':
                    subprocess.run(['open', str(projects_dir)])
                else:
                    subprocess.run(['xdg-open', str(projects_dir)])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder:\n{e}")
        else:
            messagebox.showinfo("Info", "Projects folder doesn't exist yet")
    
    def view_full_status(self):
        """Run and show full status"""
        try:
            result = subprocess.run(
                [str(self.venv_python), str(self.app_dir / "vibe_coder.py"), "status"],
                capture_output=True,
                text=True,
                cwd=str(self.app_dir)
            )
            
            # Show in new window
            status_window = tk.Toplevel(self.root)
            status_window.title("Vibe Coder Status")
            status_window.geometry("600x400")
            
            text = scrolledtext.ScrolledText(status_window, wrap=tk.WORD, font=('Courier', 10))
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text.insert(tk.END, result.stdout)
            if result.stderr:
                text.insert(tk.END, "\n" + result.stderr)
            text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not get status:\n{e}")
    
    def list_apps(self):
        """List generated apps"""
        try:
            result = subprocess.run(
                [str(self.venv_python), str(self.app_dir / "vibe_coder.py"), "list"],
                capture_output=True,
                text=True,
                cwd=str(self.app_dir)
            )
            
            # Show in new window
            apps_window = tk.Toplevel(self.root)
            apps_window.title("Generated Apps")
            apps_window.geometry("600x400")
            
            text = scrolledtext.ScrolledText(apps_window, wrap=tk.WORD, font=('Courier', 10))
            text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text.insert(tk.END, result.stdout)
            if result.stderr:
                text.insert(tk.END, "\n" + result.stderr)
            text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not list apps:\n{e}")
    
    def on_closing(self):
        """Handle window close"""
        if self.is_running:
            if messagebox.askyesno("Running Process", 
                                   "Vibe Coder is still running. Stop it and exit?"):
                self.stop_vibe_coder()
                self.root.destroy()
            else:
                # Minimize to tray or keep running
                self.root.withdraw()
        else:
            self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = VibeCoderGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
