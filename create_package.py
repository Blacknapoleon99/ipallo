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
    
    # Copy installer
    installer_dir = package_dir / "installer"
    installer_dir.mkdir(exist_ok=True)
    shutil.copy2("installer/install_blackz.py", installer_dir / "install_blackz.py")
    shutil.copy2("installer/install.bat", package_dir / "install.bat")
    print("✅ Copied installer files")
    
    # Create package README
    readme_content = f"""BlackzAllocator v{version} - Professional IP Pool Management
================================================================

🚀 What's Included:
------------------
• BlackzAllocator.exe - Main application (standalone executable)
• install.bat - Easy Windows installer
• installer/ - Installation scripts

🔧 Installation:
---------------
METHOD 1 (Recommended): 
   1. Double-click "install.bat"
   2. Follow the installation wizard
   3. Launch from desktop shortcut or Start Menu

METHOD 2 (Manual):
   1. Copy BlackzAllocator.exe to desired location
   2. Run BlackzAllocator.exe

💻 System Requirements:
----------------------
• Windows 10/11 (64-bit)
• 512 MB RAM minimum
• 100 MB disk space
• Network access for IP management

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
1. Install using install.bat
2. Launch BlackzAllocator
3. Click "Create Pool" to create your first IP pool
4. Use the Allocations tab to manage IP assignments
5. Monitor usage in the Monitoring tab

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
• Database Engine: SQLite
• GUI Framework: CustomTkinter
• API Framework: FastAPI
• Network Library: psutil

Dependencies Included:
---------------------
All required dependencies are bundled in the executable.
No additional installation required.

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
2. Run install.bat for automatic installation
3. Or manually run BlackzAllocator.exe
""")

if __name__ == "__main__":
    create_package() 