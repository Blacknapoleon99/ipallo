#!/usr/bin/env python3
"""
Create ForceBindIP GUI Distribution Package
"""

import os
import shutil
import zipfile
from pathlib import Path
import datetime

def create_package():
    """Create a distribution package for ForceBindIP GUI"""
    print("🎁 Creating ForceBindIP GUI Distribution Package...")
    
    # Package info
    version = "2.0.0"  # New version for ForceBindIP GUI
    package_name = f"ForceBindIP_GUI_v{version}_{datetime.datetime.now().strftime('%Y%m%d')}"
    
    # Create package directory
    package_dir = Path("package") / package_name
    package_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 Package directory: {package_dir}")
    
    # Copy executable
    exe_source = Path("dist/ForceBindIP_Launcher.exe")
    if exe_source.exists():
        shutil.copy2(exe_source, package_dir / "ForceBindIP_Launcher.exe")
        print(f"✅ Copied executable: {exe_source.stat().st_size / 1024 / 1024:.1f} MB")
    else:
        print("❌ Executable not found! Run PyInstaller first.")
        return
    
    # Copy icon
    icon_source = Path("blackz_icon.ico")
    if icon_source.exists():
        shutil.copy2(icon_source, package_dir / "forcebindip_icon.ico")
        print("✅ Copied icon file")
    
    # Create README file
    readme_content = """# ForceBindIP GUI Launcher v2.0.0

## 🌐 Professional Network Interface Binding Application

A modern, user-friendly GUI for ForceBindIP that allows you to bind applications to specific network interfaces.

### 📋 Features

• **Modern Dark Theme**: Beautiful CustomTkinter interface with rounded corners
• **Auto Interface Detection**: Automatically detects and lists all network interfaces
• **Application Browser**: Easy file browser to select applications to launch
• **Configuration Management**: Save and load application configurations
• **Quick Launch**: Fast access to frequently used applications
• **x86/x64 Support**: Supports both 32-bit and 64-bit ForceBindIP versions
• **Command Arguments**: Support for command line arguments
• **Delayed Injection**: Optional delayed injection mode
• **Interface Testing**: Test network interface connectivity

### 🚀 Quick Start

1. **Download ForceBindIP** (Required):
   - Visit: https://r1ch.net/projects/forcebindip
   - Download and extract ForceBindIP.exe or ForceBindIP64.exe

2. **Run the Application**:
   - Double-click `ForceBindIP_Launcher.exe`

3. **Configure ForceBindIP Path**:
   - Go to Settings tab
   - Browse for your ForceBindIP.exe location
   - Test the path to verify it works

4. **Launch Applications**:
   - Go to Launcher tab
   - Browse for application to launch
   - Select network interface
   - Click "Launch App"

### 💾 Configuration Management

Save frequently used applications as configurations:
- Select app and interface in Launcher tab
- Click "Save Config"
- Access saved configs in Configurations tab
- Use Quick Launch for instant access

### 🌐 Network Interface Binding

The application binds your chosen programs to specific network interfaces:
- Useful for VPN routing
- Force apps through specific connections
- Bypass network restrictions
- Testing with different interfaces

### ⚙️ Requirements

- Windows 10/11
- ForceBindIP (download separately)
- Network interfaces configured on your system

### 🔧 Troubleshooting

**"ForceBindIP not found" error**:
- Download ForceBindIP from official source
- Set correct path in Settings tab
- Ensure executable permissions

**"Interface not found" error**:
- Check network adapter status
- Refresh interfaces in Interfaces tab
- Verify interface has valid IP address

**Application fails to launch**:
- Check if application path is correct
- Verify ForceBindIP version matches target app (x86/x64)
- Try delayed injection mode
- Check application permissions

### 📝 Version History

**v2.0.0** - Complete ForceBindIP GUI Implementation
- Modern CustomTkinter interface
- Auto network interface detection
- Configuration management system
- Quick launch functionality
- Interface testing and validation
- x86/x64 ForceBindIP support

### 📄 License

This application is provided as-is. ForceBindIP is created by Richard Stanway.

### 🌐 Links

- ForceBindIP Official: https://r1ch.net/projects/forcebindip
- GitHub Repository: https://github.com/Blacknapoleon99/ipallo

---
Created with ❤️ for the networking community
"""
    
    with open(package_dir / "README.txt", 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("✅ Created README.txt")
    
    # Create simple installer batch file
    installer_content = """@echo off
title ForceBindIP GUI Installer
color 0B

echo.
echo ===============================================
echo    ForceBindIP GUI Simple Installer
echo    Professional Network Interface Binding
echo ===============================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo [INFO] Installing ForceBindIP GUI Launcher...
echo [DEBUG] Current directory: %CD%

REM Create installation directory
set "INSTALL_DIR=%USERPROFILE%\\AppData\\Local\\ForceBindIP_GUI"
echo [INFO] Installation directory: %INSTALL_DIR%

if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo [OK] Created installation directory
)

REM Copy files
if exist "ForceBindIP_Launcher.exe" (
    copy "ForceBindIP_Launcher.exe" "%INSTALL_DIR%\\" >nul
    echo [OK] Copied ForceBindIP_Launcher.exe
) else (
    echo [ERROR] ForceBindIP_Launcher.exe not found!
    pause
    exit /b 1
)

if exist "forcebindip_icon.ico" (
    copy "forcebindip_icon.ico" "%INSTALL_DIR%\\" >nul
    echo [OK] Copied application icon
)

if exist "README.txt" (
    copy "README.txt" "%INSTALL_DIR%\\" >nul
    echo [OK] Copied README file
)

REM Create desktop shortcut
set "DESKTOP=%USERPROFILE%\\Desktop"
echo [INFO] Creating desktop shortcut...

echo [Desktop Entry] > "%DESKTOP%\\ForceBindIP GUI.url"
echo URL=file:///%INSTALL_DIR%\\ForceBindIP_Launcher.exe >> "%DESKTOP%\\ForceBindIP GUI.url"
echo IconFile=%INSTALL_DIR%\\forcebindip_icon.ico >> "%DESKTOP%\\ForceBindIP GUI.url"

REM Alternative shortcut creation using PowerShell
powershell -Command "^
$WshShell = New-Object -comObject WScript.Shell; ^
$Shortcut = $WshShell.CreateShortcut('%DESKTOP%\\ForceBindIP GUI.lnk'); ^
$Shortcut.TargetPath = '%INSTALL_DIR%\\ForceBindIP_Launcher.exe'; ^
$Shortcut.WorkingDirectory = '%INSTALL_DIR%'; ^
$Shortcut.IconLocation = '%INSTALL_DIR%\\forcebindip_icon.ico'; ^
$Shortcut.Description = 'ForceBindIP GUI Launcher'; ^
$Shortcut.Save()" 2>nul

if exist "%DESKTOP%\\ForceBindIP GUI.lnk" (
    echo [OK] Desktop shortcut created
) else (
    echo [WARN] Could not create desktop shortcut
)

echo.
echo ===============================================
echo Installation completed successfully!
echo.
echo You can now:
echo 1. Use the desktop shortcut: "ForceBindIP GUI"
echo 2. Run directly from: %INSTALL_DIR%\\ForceBindIP_Launcher.exe
echo.
echo IMPORTANT: Download ForceBindIP from:
echo https://r1ch.net/projects/forcebindip
echo.
echo Configure the ForceBindIP path in Settings tab
echo ===============================================
echo.

REM Offer to launch the application
set /p launch="Launch ForceBindIP GUI now? (Y/N): "
if /i "%launch%"=="Y" (
    echo [INFO] Launching ForceBindIP GUI...
    start "" "%INSTALL_DIR%\\ForceBindIP_Launcher.exe"
) else (
    echo [INFO] You can launch it later from the desktop shortcut
)

echo.
echo Press any key to exit...
pause >nul
"""
    
    with open(package_dir / "INSTALL.bat", 'w', encoding='utf-8') as f:
        f.write(installer_content)
    print("✅ Created INSTALL.bat")
    
    # Create VERSION file
    version_content = f"""ForceBindIP GUI Launcher v{version}
Build Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Application Type: Network Interface Binding GUI
ForceBindIP Integration: Professional
Platform: Windows 10/11
Architecture: x64

Features:
- Modern CustomTkinter interface
- Auto network interface detection  
- Configuration management
- Quick launch system
- x86/x64 ForceBindIP support
- Interface testing and validation

Requirements:
- Windows 10 or later
- ForceBindIP (download separately)
- Network adapters configured

For latest updates visit:
https://github.com/Blacknapoleon99/ipallo
"""
    
    with open(package_dir / "VERSION.txt", 'w', encoding='utf-8') as f:
        f.write(version_content)
    print("✅ Created VERSION.txt")
    
    # Create the ZIP package
    zip_path = Path(f"{package_name}.zip")
    print(f"📦 Creating ZIP package: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in package_dir.rglob('*'):
            if file_path.is_file():
                arc_name = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_name)
                print(f"   + {arc_name}")
    
    # Get file sizes
    exe_size = (package_dir / "ForceBindIP_Launcher.exe").stat().st_size / 1024 / 1024
    zip_size = zip_path.stat().st_size / 1024 / 1024
    
    print(f"\n🎉 Package created successfully!")
    print(f"📊 Package Statistics:")
    print(f"   • Executable size: {exe_size:.1f} MB")
    print(f"   • ZIP package size: {zip_size:.1f} MB")
    print(f"   • Package location: {zip_path.absolute()}")
    print(f"   • Version: v{version}")
    
    print(f"\n📋 Package Contents:")
    print(f"   • ForceBindIP_Launcher.exe - Main application")
    print(f"   • INSTALL.bat - Simple installer")
    print(f"   • README.txt - User guide and instructions")
    print(f"   • VERSION.txt - Version information")
    print(f"   • forcebindip_icon.ico - Application icon")
    
    print(f"\n✅ Ready for distribution!")
    print(f"🌐 Users can download and run INSTALL.bat to install")
    
    return zip_path

if __name__ == "__main__":
    create_package() 