#!/usr/bin/env python3
"""
Complete BlackzAllocator Application Launcher
Starts both API server and GUI together
"""

import sys
import os
import time
import threading
import subprocess
import requests

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def start_api_server():
    """Start the API server in a separate thread"""
    print("🚀 Starting API server...")
    try:
        # Initialize database first
        from database import init_database
        init_database()
        print("✅ Database initialized")
        
        # Import and start API server
        import uvicorn
        from api.main import app
        
        # Start server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="error",  # Reduce log noise
            access_log=False,
            reload=False
        )
    except Exception as e:
        print(f"❌ API Server error: {e}")

def wait_for_api_server(max_attempts=30):
    """Wait for API server to be ready"""
    print("⏳ Waiting for API server to start...")
    for attempt in range(max_attempts):
        try:
            response = requests.get("http://localhost:8000/health", timeout=1)
            if response.status_code == 200:
                print("✅ API server is ready!")
                return True
        except:
            pass
        time.sleep(1)
        if attempt % 5 == 0:
            print(f"   Still waiting... (attempt {attempt + 1}/{max_attempts})")
    
    print("❌ API server failed to start in time")
    return False

def start_gui():
    """Start the GUI"""
    print("🎨 Starting GUI...")
    try:
        from gui.modern_window import ModernBlackzAllocatorGUI
        app = ModernBlackzAllocatorGUI()
        print("✨ GUI is ready!")
        app.run()
    except Exception as e:
        print(f"❌ GUI error: {e}")

def main():
    """Main launcher - starts API server and GUI"""
    print("=" * 60)
    print("    BlackzAllocator Complete Application")
    print("    Professional IP Pool Management System")
    print("=" * 60)
    print()
    
    try:
        # Start API server in background thread
        api_thread = threading.Thread(target=start_api_server, daemon=True)
        api_thread.start()
        
        # Wait for API server to be ready
        if wait_for_api_server():
            print("🚀 Starting complete application...")
            time.sleep(1)  # Small delay to ensure API is stable
            
            # Start GUI in main thread
            start_gui()
        else:
            print("❌ Failed to start API server - GUI may not function properly")
            print("💡 Try running: python api_server.py separately")
            
            # Start GUI anyway (with API disconnected status)
            start_gui()
            
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 