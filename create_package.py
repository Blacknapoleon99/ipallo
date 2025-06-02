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
    version = "1.0.0"
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
    
    # Copy simple installer (main installer)
    shutil.copy2("simple_install.py", package_dir / "install.py")
    print("✅ Copied simple installer as install.py")
    
    # Copy complex installer as backup
    installer_dir = package_dir / "installer"
    installer_dir.mkdir(exist_ok=True)
    shutil.copy2("installer/install_blackz.py", installer_dir / "install_blackz.py")
    shutil.copy2("installer/install.bat", package_dir / "install.bat")
    print("✅ Copied complex installer files")
    
    # Create a simple batch file for the simple installer
    simple_batch = package_dir / "INSTALL.bat"
    with open(simple_batch, 'w') as f:
        f.write('''@echo off
title BlackzAllocator Simple Installer
color 0B

echo.
echo ===============================================
echo    BlackzAllocator Simple Installer
echo    Professional IP Pool Management System
echo ===============================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python from https://python.org
    pause
    exit /b 1
)

echo [INFO] Starting simple installation...
python install.py

pause
''')
    print("✅ Created INSTALL.bat for simple installer")
    
    # Create package README
    readme_content = f"""BlackzAllocator v{version} - Professional IP Pool Management
================================================================

🚀 What's Included:
------------------
• BlackzAllocator.exe - Main application (standalone executable)
• INSTALL.bat - Simple installer (RECOMMENDED)
• install.bat - Advanced installer (backup)
• install.py - Simple Python installer
• installer/ - Advanced installation scripts

🔧 Installation Options:
------------------------
METHOD 1 (RECOMMENDED - Simple): 
   1. Double-click "INSTALL.bat"
   2. Follow the simple installation wizard
   3. Launch from desktop shortcut

METHOD 2 (Advanced):
   1. Double-click "install.bat" 
   2. Follow the advanced installation wizard

METHOD 3 (Manual):
   1. Copy BlackzAllocator.exe to desired location
   2. Run BlackzAllocator.exe directly

💻 System Requirements:
----------------------
• Windows 10/11 (64-bit)
• 512 MB RAM minimum
• 100 MB disk space
• Python (for installer only - not needed to run the app)

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
1. Use INSTALL.bat for easiest installation
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
or check the project documentation.

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
• Simple Installer: INSTALL.bat + install.py
• Advanced Installer: install.bat + installer/install_blackz.py
• Database Engine: SQLite (embedded)
• GUI Framework: CustomTkinter
• API Framework: FastAPI
• Network Library: psutil

Installation Options:
--------------------
1. INSTALL.bat - Simple, reliable installer (recommended)
2. install.bat - Advanced installer with more features
3. Manual - Just run BlackzAllocator.exe directly

Dependencies Included:
---------------------
All required dependencies are bundled in the executable.
No additional installation required to run the application.

Installation Size: ~150 MB
Runtime Memory: ~50-100 MB
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
2. Run INSTALL.bat for simple installation (RECOMMENDED)
3. Run install.bat for advanced installation
4. Or manually run BlackzAllocator.exe directly

🎯 Installation Options:
- INSTALL.bat: Simple, foolproof installer
- install.bat: Advanced installer with more features
- Manual: No installation needed
""")

if __name__ == "__main__":
    create_package() 