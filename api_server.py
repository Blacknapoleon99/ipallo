#!/usr/bin/env python3
"""
BlackzAllocator API Server Entry Point

This script starts only the API server without the GUI.
Useful for server deployments or API-only usage.
"""

import sys
import os
import uvicorn

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the API server"""
    print("Starting BlackzAllocator API Server...")
    
    # Initialize database
    try:
        from database import init_database
        init_database()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
        return
    
    # Import the FastAPI app
    from api.main import app
    
    # Start the server
    try:
        uvicorn.run(
            app,
            host="127.0.0.1",  # Changed from 0.0.0.0 to 127.0.0.1 for localhost access
            port=8000,
            log_level="info",
            reload=False,  # Set to True for development
            access_log=True
        )
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")

if __name__ == "__main__":
    main() 