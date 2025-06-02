#!/usr/bin/env python3
"""
Modern BlackzAllocator GUI Starter
Uses customtkinter for modern rounded corners and sleek design
"""

import sys
import os
import customtkinter as ctk
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
    """Start modern GUI directly"""
    print("🚀 Starting Modern BlackzAllocator GUI...")
    
    try:
        # Initialize database
        from database import init_database
        init_database()
        print("✅ Database initialized")
        
        # Import and start modern GUI
        from gui.modern_window import ModernBlackzAllocatorGUI
        
        print("🎨 Creating modern GUI window...")
        app = ModernBlackzAllocatorGUI()
        
        # Check API connection and update status
        def update_connection_status():
            if check_api_connection():
                app.status_label.configure(text="Connected")
                app.status_dot.configure(text_color="#40ff40")
                print("✓ Connected to API server")
            else:
                app.status_label.configure(text="API Disconnected")
                app.status_dot.configure(text_color="#ff6b6b")
                print("⚠ API server not detected - start with: python api_server.py")
        
        # Initial status check
        app.root.after(1000, update_connection_status)
        
        # Check connection status every 5 seconds
        def periodic_check():
            update_connection_status()
            app.root.after(5000, periodic_check)
        
        app.root.after(2000, periodic_check)  # Start checking after 2 seconds
        
        print("✨ Modern GUI window is now ready!")
        print("📱 Features: Rounded corners, smooth animations, modern design")
        
        # Start GUI loop
        app.run()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        # Create a simple error dialog using customtkinter
        ctk.set_appearance_mode("dark")
        error_window = ctk.CTk()
        error_window.title("Error")
        error_window.geometry("400x200")
        
        error_label = ctk.CTkLabel(
            error_window, 
            text=f"Failed to start GUI:\n{str(e)}", 
            font=ctk.CTkFont(size=14)
        )
        error_label.pack(pady=20)
        
        close_button = ctk.CTkButton(
            error_window, 
            text="Close", 
            command=error_window.destroy,
            corner_radius=10
        )
        close_button.pack(pady=10)
        
        error_window.mainloop()

if __name__ == "__main__":
    main() 