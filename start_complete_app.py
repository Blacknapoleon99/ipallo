#!/usr/bin/env python3
"""
Complete ForceBindIP Application Launcher
Launches the ForceBindIP GUI application
"""

import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Start the complete ForceBindIP application"""
    print("🌐 Starting ForceBindIP Launcher...")
    print("=" * 50)
    
    try:
        # Import and start the ForceBindIP GUI
        from gui.modern_window import ModernForceBindIPGUI
        
        print("🎨 Initializing modern GUI...")
        app = ModernForceBindIPGUI()
        
        print("🔄 Loading configuration and network interfaces...")
        # Initialize with data refresh
        app.refresh_all_data()
        app.refresh_quick_launch()
        
        print("✅ ForceBindIP GUI ready!")
        print("📋 Features:")
        print("  • Modern dark theme with rounded corners")
        print("  • Automatic network interface detection")
        print("  • Configuration saving and quick launch")
        print("  • x86/x64 ForceBindIP support")
        print("  • Application browsing and argument support")
        print("=" * 50)
        
        # Run the GUI
        app.root.mainloop()
        
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        sys.exit(0)
    except ImportError as e:
        print(f"❌ Import Error: {str(e)}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install customtkinter psutil")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 