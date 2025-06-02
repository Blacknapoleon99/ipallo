#!/usr/bin/env python3
"""
BlackzAllocator Simple Installer
Professional IP Pool Management System
"""

import os
import shutil
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("    BlackzAllocator Simple Installer")
    print("    Professional IP Pool Management System")
    print("=" * 60)
    print()
    
    # Find BlackzAllocator.exe in the same directory as this script
    script_dir = Path(__file__).parent.absolute()
    exe_path = script_dir / "BlackzAllocator.exe"
    
    print(f"Looking for BlackzAllocator.exe at: {exe_path}")
    
    if not exe_path.exists():
        print("❌ BlackzAllocator.exe not found in the same directory as this installer!")
        print(f"   Script directory: {script_dir}")
        print("   Directory contents:")
        for item in script_dir.iterdir():
            print(f"     - {item.name}")
        input("\nPress Enter to exit...")
        return
    
    print("✅ Found BlackzAllocator.exe")
    
    # Default installation directory
    if os.name == 'nt':  # Windows
        default_install_path = Path.home() / "AppData" / "Local" / "BlackzAllocator"
    else:  # Linux/Mac
        default_install_path = Path.home() / ".local" / "share" / "BlackzAllocator"
    
    print(f"\nDefault installation path: {default_install_path}")
    print()
    
    # Ask user for installation path
    custom_path = input("Press Enter to use default path, or enter custom path: ").strip()
    
    if custom_path:
        install_path = Path(custom_path)
    else:
        install_path = default_install_path
    
    print(f"\n📁 Installing to: {install_path}")
    
    try:
        # Create installation directory
        install_path.mkdir(parents=True, exist_ok=True)
        
        # Copy executable
        exe_dest = install_path / "BlackzAllocator.exe"
        shutil.copy2(exe_path, exe_dest)
        print("✅ Copied BlackzAllocator.exe")
        
        # Create desktop shortcut (Windows)
        if os.name == 'nt':
            try:
                # Simple shortcut creation without external dependencies
                desktop = Path.home() / "Desktop"
                if desktop.exists():
                    # Create a simple batch file shortcut
                    shortcut_path = desktop / "BlackzAllocator.bat"
                    with open(shortcut_path, 'w') as f:
                        f.write(f'@echo off\n')
                        f.write(f'cd /d "{install_path}"\n')
                        f.write(f'start "" "BlackzAllocator.exe"\n')
                    print("✅ Created desktop shortcut (BlackzAllocator.bat)")
                else:
                    print("⚠️  Desktop folder not found")
            except Exception as e:
                print(f"⚠️  Desktop shortcut creation failed: {e}")
        
        # Create README
        readme_path = install_path / "README.txt"
        with open(readme_path, 'w') as f:
            f.write("""BlackzAllocator - Professional IP Pool Management
=====================================================

Installation Complete!

What is BlackzAllocator?
-----------------------
BlackzAllocator is a professional IP pool management system with:
• Modern graphical interface with rounded corners
• IP pool creation and management
• Dynamic IP allocation with multiple strategies
• Network interface binding
• Real-time monitoring and statistics
• Professional dark theme design

How to Run:
----------
1. Double-click BlackzAllocator.exe
2. Or run from desktop shortcut
3. Or launch from: {install_path}

Features:
--------
• Create and manage IP pools (CIDR networks)
• Allocate IPs dynamically (first-fit, random, sequential, load-balanced)
• Reserve specific IP addresses
• Monitor utilization and statistics
• Clean modern interface inspired by macOS/Flutter apps

Enjoy using BlackzAllocator!
""")
        
        print("✅ Created README.txt")
        
        print("\n🎉 Installation Complete!")
        print(f"📍 BlackzAllocator installed to: {install_path}")
        print("🚀 You can now run BlackzAllocator from:")
        print("   • Desktop shortcut")
        print(f"   • Directly: {exe_dest}")
        
        # Ask if user wants to launch immediately
        launch = input("\n🚀 Launch BlackzAllocator now? (Y/n): ").strip()
        if launch.lower() != 'n':
            try:
                subprocess.Popen([str(exe_dest)], cwd=str(install_path))
                print("✅ BlackzAllocator launched!")
            except Exception as e:
                print(f"❌ Failed to launch: {e}")
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return
    
    print("\n🎯 Thank you for choosing BlackzAllocator!")
    input("\nPress Enter to exit installer...")

if __name__ == "__main__":
    main() 