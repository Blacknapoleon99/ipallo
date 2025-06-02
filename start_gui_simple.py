#!/usr/bin/env python3
"""
Simple BlackzAllocator GUI Starter
Bypasses API server auto-detection and starts GUI directly
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import requests
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_api_connection():
    """Check if API server is accessible"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def main():
    """Start GUI directly"""
    print("Starting BlackzAllocator GUI...")
    
    try:
        # Initialize database
        from database import init_database
        init_database()
        print("Database initialized")
        
        # Import and start GUI
        from gui.main_window import BlackzAllocatorGUI
        
        print("Creating GUI window...")
        app = BlackzAllocatorGUI()
        
        # Make window visible and on top
        app.root.lift()
        app.root.attributes('-topmost', True)
        app.root.after_idle(app.root.attributes, '-topmost', False)
        app.root.focus_force()
        
        # Check API connection and update status
        def update_connection_status():
            if check_api_connection():
                app.status_label.config(text="Connected", foreground='#00d26a')
                print("✓ Connected to API server")
            else:
                app.status_label.config(text="API Disconnected", foreground='#ff6b6b')
                print("⚠ API server not detected - start with: python api_server.py")
        
        # Initial status check
        update_connection_status()
        
        # Check connection status every 5 seconds
        def periodic_check():
            update_connection_status()
            app.root.after(5000, periodic_check)
        
        app.root.after(1000, periodic_check)  # Start checking after 1 second
        
        print("GUI window should now be visible!")
        
        # Start GUI loop
        app.run()
        
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Failed to start GUI:\n{str(e)}")

if __name__ == "__main__":
    main() 