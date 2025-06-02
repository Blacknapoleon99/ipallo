#!/usr/bin/env python3
"""
BlackzAllocator Installer
Professional IP Pool Management System
"""

import os
import shutil
import sys
import zipfile
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("    BlackzAllocator Installer")
    print("    Professional IP Pool Management System")
    print("=" * 60)
    print()
    
    # Default installation directory
    if os.name == 'nt':  # Windows
        default_install_path = Path.home() / "AppData" / "Local" / "BlackzAllocator"
    else:  # Linux/Mac
        default_install_path = Path.home() / ".local" / "share" / "BlackzAllocator"
    
    print(f"Default installation path: {default_install_path}")
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
        exe_source = Path("dist/BlackzAllocator.exe")
        if exe_source.exists():
            exe_dest = install_path / "BlackzAllocator.exe"
            shutil.copy2(exe_source, exe_dest)
            print("✅ Copied BlackzAllocator.exe")
        else:
            print("❌ BlackzAllocator.exe not found. Please build first!")
            return
        
        # Create desktop shortcut (Windows)
        if os.name == 'nt':
            try:
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                shortcut_path = os.path.join(desktop, "BlackzAllocator.lnk")
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.Targetpath = str(exe_dest)
                shortcut.WorkingDirectory = str(install_path)
                shortcut.IconLocation = str(exe_dest)
                shortcut.save()
                
                print("✅ Created desktop shortcut")
            except ImportError:
                print("⚠️  Desktop shortcut creation skipped (winshell not available)")
        
        # Create start menu entry (Windows)
        if os.name == 'nt':
            try:
                start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
                start_menu_shortcut = start_menu / "BlackzAllocator.lnk"
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(str(start_menu_shortcut))
                shortcut.Targetpath = str(exe_dest)
                shortcut.WorkingDirectory = str(install_path)
                shortcut.IconLocation = str(exe_dest)
                shortcut.save()
                
                print("✅ Created Start Menu entry")
            except Exception as e:
                print(f"⚠️  Start Menu entry creation failed: {e}")
        
        # Create uninstaller
        uninstall_script = install_path / "uninstall.py"
        with open(uninstall_script, 'w') as f:
            f.write(f'''#!/usr/bin/env python3
"""
BlackzAllocator Uninstaller
"""

import os
import shutil
import sys
from pathlib import Path

def main():
    print("BlackzAllocator Uninstaller")
    print("=" * 30)
    
    confirm = input("Are you sure you want to uninstall BlackzAllocator? (y/N): ")
    if confirm.lower() != 'y':
        print("Uninstall cancelled.")
        return
    
    install_path = Path(r"{install_path}")
    
    try:
        # Remove desktop shortcut
        try:
            import winshell
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "BlackzAllocator.lnk")
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                print("✅ Removed desktop shortcut")
        except:
            pass
        
        # Remove start menu entry
        try:
            start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
            start_menu_shortcut = start_menu / "BlackzAllocator.lnk"
            if start_menu_shortcut.exists():
                start_menu_shortcut.unlink()
                print("✅ Removed Start Menu entry")
        except:
            pass
        
        # Remove installation directory
        if install_path.exists():
            shutil.rmtree(install_path)
            print("✅ Removed installation directory")
        
        print("\\n🎯 BlackzAllocator has been successfully uninstalled!")
        
    except Exception as e:
        print(f"❌ Error during uninstall: {{e}}")
    
    input("\\nPress Enter to exit...")

if __name__ == "__main__":
    main()
''')
        
        print("✅ Created uninstaller")
        
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
2. Or run from Start Menu: BlackzAllocator
3. Or run from desktop shortcut

Features:
--------
• Create and manage IP pools (CIDR networks)
• Allocate IPs dynamically (first-fit, random, sequential, load-balanced)
• Reserve specific IP addresses
• Monitor utilization and statistics
• Clean modern interface inspired by macOS/Flutter apps

Support:
-------
For questions or issues, refer to the project documentation.

Uninstall:
---------
Run uninstall.py in the installation directory or use Windows Add/Remove Programs.

Enjoy using BlackzAllocator!
""")
        
        print("✅ Created README.txt")
        
        print("\n🎉 Installation Complete!")
        print(f"📍 BlackzAllocator installed to: {install_path}")
        print("🚀 You can now run BlackzAllocator from:")
        print("   • Desktop shortcut")
        print("   • Start Menu")
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
        return
    
    print("\n🎯 Thank you for choosing BlackzAllocator!")
    input("\nPress Enter to exit installer...")

if __name__ == "__main__":
    main() 