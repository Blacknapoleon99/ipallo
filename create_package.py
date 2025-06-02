#!/usr/bin/env python3
"""
Create BlackzAllocator Distribution Package
"""

import os
import shutil
import zipfile
from pathlib import Path
import datetime

def create_package():
    """Create a distribution package for BlackzAllocator"""
    print("🎁 Creating BlackzAllocator Distribution Package...")
    
    # Package info
    version = "1.0.1"  # Updated version with installer fixes
    package_name = f"BlackzAllocator_v{version}_{datetime.datetime.now().strftime('%Y%m%d')}"
    
    # Create package directory
    package_dir = Path("package") / package_name
    package_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Package directory: {package_dir}")
    
    # Copy executable
    exe_source = Path("dist/BlackzAllocator.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, package_dir / "BlackzAllocator.exe")
        print("✅ Copied BlackzAllocator.exe")
    else:
        print("❌ BlackzAllocator.exe not found. Please build first!")
        return
    
    # Copy super simple installer (main installer)
    shutil.copy2("INSTALL_SIMPLE.bat", package_dir / "INSTALL_SIMPLE.bat")
    print("✅ Copied super simple batch installer")
    
    # Copy simple installer (Python version)
    shutil.copy2("simple_install.py", package_dir / "install.py")
    print("✅ Copied simple Python installer")
    
    # Copy complex installer as backup
    installer_dir = package_dir / "installer"
    installer_dir.mkdir(exist_ok=True)
    shutil.copy2("installer/install_blackz.py", installer_dir / "install_blackz.py")
    shutil.copy2("installer/install.bat", package_dir / "install.bat")
    print("✅ Copied complex installer files")
    
    # Create a simple batch file for the Python installer
    simple_batch = package_dir / "INSTALL.bat"
    with open(simple_batch, 'w') as f:
        f.write('''@echo off
title BlackzAllocator Python Installer
color 0B

echo.
echo ===============================================
echo    BlackzAllocator Python Installer
echo    Professional IP Pool Management System
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python from https://python.org
    echo [INFO] OR use INSTALL_SIMPLE.bat instead (no Python required)
    pause
    exit /b 1
)

echo [INFO] Starting Python installation...
python install.py

pause
''')
    print("✅ Created INSTALL.bat for Python installer")
    
    # Create package README
    readme_content = f"""BlackzAllocator v{version} - Professional IP Pool Management
================================================================

🚀 What's Included:
------------------
• BlackzAllocator.exe - Main application (standalone executable)
• INSTALL_SIMPLE.bat - Super simple installer (NO PYTHON NEEDED) ⭐ RECOMMENDED
• INSTALL.bat - Python installer (requires Python)
• install.py - Python installer script
• install.bat - Advanced installer (backup)
• installer/ - Advanced installation scripts

🔧 Installation Options:
------------------------
METHOD 1 (SUPER SIMPLE - RECOMMENDED): 
   1. Double-click "INSTALL_SIMPLE.bat"
   2. No Python required!
   3. Automatically finds BlackzAllocator.exe
   4. Creates desktop shortcut

METHOD 2 (Python installer):
   1. Double-click "INSTALL.bat" 
   2. Requires Python installed
   3. More robust searching

METHOD 3 (Advanced):
   1. Double-click "install.bat"
   2. Advanced features

METHOD 4 (Manual):
   1. Copy BlackzAllocator.exe to desired location
   2. Run BlackzAllocator.exe directly

💻 System Requirements:
----------------------
• Windows 10/11 (64-bit)
• 512 MB RAM minimum
• 100 MB disk space
• NO additional software required to run the app!
• Python only needed for INSTALL.bat (not for INSTALL_SIMPLE.bat)

✨ Features:
-----------
• Modern GUI with rounded corners and dark theme
• Create and manage IP pools (CIDR networks)
• Dynamic IP allocation with multiple strategies:
  - First-fit allocation
  - Random allocation
  - Sequential allocation
  - Load-balanced allocation
• Reserve specific IP addresses
• Network interface binding and testing
• Real-time monitoring and statistics
• Professional interface inspired by macOS/Flutter

🎯 Quick Start:
--------------
1. Use INSTALL_SIMPLE.bat for easiest installation (no Python needed!)
2. Launch BlackzAllocator
3. Click "Create Pool" to create your first IP pool
4. Use the interface to manage IP assignments
5. Monitor usage in real-time

🛠️ Network Management:
----------------------
• Pool Management: Create, edit, delete IP pools
• IP Allocation: Dynamic and static IP assignment
• Interface Binding: Bind IPs to network interfaces
• Utilization Tracking: Monitor pool usage in real-time
• Lease Management: Handle IP lease durations and renewals

📞 Support:
----------
For technical support or questions, refer to the application's help system
or check the project documentation at: https://github.com/Blacknapoleon99/ipallo

🎉 Thank you for choosing BlackzAllocator!

Version: {version}
Build Date: {datetime.datetime.now().strftime('%Y-%m-%d')}
"""
    
    with open(package_dir / "README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ Created README.txt")
    
    # Create version info
    version_info = f"""BlackzAllocator Version Information
===================================

Version: {version}
Build Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Build Type: Release
Architecture: x64
Platform: Windows

Components:
-----------
• Main Application: BlackzAllocator.exe
• Super Simple Installer: INSTALL_SIMPLE.bat (no Python needed)
• Python Installer: INSTALL.bat + install.py
• Advanced Installer: install.bat + installer/install_blackz.py
• Database Engine: SQLite (embedded)
• GUI Framework: CustomTkinter
• API Framework: FastAPI
• Network Library: psutil

Installation Options:
--------------------
1. INSTALL_SIMPLE.bat - Super simple, no Python needed (RECOMMENDED)
2. INSTALL.bat - Python installer with robust searching  
3. install.bat - Advanced installer with more features
4. Manual - Just run BlackzAllocator.exe directly

Dependencies Included:
---------------------
All required dependencies are bundled in the executable.
No additional installation required to run the application.

Installation Size: ~150 MB
Runtime Memory: ~50-100 MB

Fixed in v{version}:
-------------------
• Fixed installer path detection issues
• Added super simple batch installer (no Python required)
• Improved executable search algorithm
• Better error messages and debugging
• Multiple installation fallback options
"""
    
    with open(package_dir / "VERSION.txt", 'w', encoding='utf-8') as f:
        f.write(version_info)
    print("✅ Created VERSION.txt")
    
    # Create ZIP package
    zip_path = f"{package_name}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arcname)
    
    print(f"✅ Created ZIP package: {zip_path}")
    
    # Get file sizes
    exe_size = exe_source.stat().st_size / 1024 / 1024
    zip_size = Path(zip_path).stat().st_size / 1024 / 1024
    
    print(f"""
🎉 Package Creation Complete!
============================
📦 Package: {package_name}
📁 Directory: {package_dir}
🗜️  ZIP File: {zip_path}
📏 Executable Size: {exe_size:.1f} MB
📏 Package Size: {zip_size:.1f} MB

🚀 Ready for Distribution!
=========================
Your friend can now:
1. Download and extract {zip_path}
2. Run INSTALL_SIMPLE.bat (RECOMMENDED - no Python needed!)
3. Run INSTALL.bat (requires Python)
4. Run install.bat (advanced installation)
5. Or manually run BlackzAllocator.exe directly

🎯 Installation Options:
- INSTALL_SIMPLE.bat: Super simple, no dependencies
- INSTALL.bat: Python installer with robust searching
- install.bat: Advanced installer with more features
- Manual: No installation needed
""")

if __name__ == "__main__":
    create_package() 