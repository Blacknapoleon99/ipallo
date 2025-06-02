#!/usr/bin/env python3
"""
BlackzAllocator GUI Application Entry Point

This script starts the BlackzAllocator GUI application.
Run this file to launch the user-friendly interface for IP pool management.
"""

import sys
import os
import threading
import time
import subprocess
import tkinter as tk
from tkinter import messagebox

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_api_server():
    """Check if API server is running"""
    import requests
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_api_server():
    """Start the API server in background"""
    try:
        # Import and start the API server
        import uvicorn
        from api.main import app
        
        def run_server():
            try:
                uvicorn.run(app, host="127.0.0.1", port=8000, log_level="error")
            except Exception as e:
                print(f"Server startup error: {e}")
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        for i in range(15):  # Wait up to 15 seconds
            time.sleep(1)
            if check_api_server():
                return True
        
        return False
    except Exception as e:
        print(f"Error starting API server: {e}")
        return False

def start_gui_only():
    """Start GUI without API server (for testing or if server is external)"""
    try:
        from gui.main_window import BlackzAllocatorGUI
        
        # Create and configure the GUI
        app = BlackzAllocatorGUI()
        
        # Make sure window appears on top
        app.root.lift()
        app.root.attributes('-topmost', True)
        app.root.after_idle(app.root.attributes, '-topmost', False)
        
        # Update status
        app.status_label.config(text="Connected to API", foreground='#90ee90')
        
        print("GUI started successfully!")
        app.run()
        
    except Exception as e:
        print(f"GUI Error: {e}")
        messagebox.showerror("GUI Error", f"Failed to start GUI:\n{str(e)}")

def main():
    """Main application entry point"""
    print("Starting BlackzAllocator...")
    
    # Initialize database first
    try:
        from database import init_database
        init_database()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization warning: {e}")
    
    # Check if API server is already running
    api_running = check_api_server()
    
    if not api_running:
        print("API server not running. Starting server...")
        
        # Try to start API server
        server_started = start_api_server()
        
        if not server_started:
            # Show option to continue without API or start manually
            root = tk.Tk()
            root.withdraw()  # Hide main window
            
            choice = messagebox.askyesnocancel(
                "API Server Issue", 
                "Failed to start API server automatically.\n\n"
                "Options:\n"
                "• YES: Start GUI only (you can start API server manually)\n"
                "• NO: Exit and start API server manually first\n"
                "• CANCEL: Exit\n\n"
                "To start API server manually:\n"
                "python api_server.py"
            )
            
            root.destroy()
            
            if choice is True:  # YES - start GUI only
                print("Starting GUI without API server...")
            elif choice is False:  # NO - exit
                print("Please start the API server manually: python api_server.py")
                return
            else:  # CANCEL
                return
    else:
        print("API server is already running.")
    
    # Start GUI application
    print("Starting GUI...")
    start_gui_only()

if __name__ == "__main__":
    main() 