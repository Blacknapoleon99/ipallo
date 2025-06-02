#!/usr/bin/env python3
"""
Modern ForceBindIP GUI Launcher
Professional Network Interface Binding Application
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Launch the modern ForceBindIP GUI"""
    print("🌐 Starting ForceBindIP Launcher...")
    
    try:
        from gui.modern_window import ModernForceBindIPGUI
        
        # Create and run the modern GUI
        app = ModernForceBindIPGUI()
        
        # Initialize with data refresh
        app.refresh_all_data()
        app.refresh_quick_launch()
        
        print("✅ ForceBindIP GUI initialized successfully")
        
        # Run the application
        app.root.mainloop()
        
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting ForceBindIP GUI: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 