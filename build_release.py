#!/usr/bin/env python3
"""
BlackzAllocator Complete Build Script
Automates the entire build and packaging process
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔨 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout.strip():
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False

def main():
    print("=" * 60)
    print("    BlackzAllocator Complete Build System")
    print("    Professional IP Pool Management")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("start_modern_gui.py").exists():
        print("❌ Please run this script from the BlackzAllocator root directory")
        sys.exit(1)
    
    print("\n📋 Build Steps:")
    print("1. Install/Update dependencies")
    print("2. Create application icon")
    print("3. Build standalone executable")
    print("4. Create distribution package")
    print("5. Test executable")
    
    proceed = input("\nProceed with build? (Y/n): ").strip()
    if proceed.lower() == 'n':
        print("Build cancelled.")
        sys.exit(0)
    
    # Step 1: Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    if not run_command("pip install pyinstaller", "Installing PyInstaller"):
        print("❌ Failed to install PyInstaller")
        sys.exit(1)
    
    # Step 2: Create icon
    if not run_command("python create_icon.py", "Creating application icon"):
        print("❌ Failed to create icon")
        sys.exit(1)
    
    # Step 3: Clean previous builds
    print("\n🧹 Cleaning previous builds...")
    for dir_name in ["build", "dist"]:
        if Path(dir_name).exists():
            import shutil
            shutil.rmtree(dir_name)
            print(f"✅ Cleaned {dir_name}/")
    
    # Step 4: Build executable
    if not run_command("python -m PyInstaller blackz_allocator.spec", "Building standalone executable"):
        print("❌ Failed to build executable")
        sys.exit(1)
    
    # Step 5: Verify executable was created
    exe_path = Path("dist/BlackzAllocator.exe")
    if not exe_path.exists():
        print("❌ Executable not found after build")
        sys.exit(1)
    
    exe_size = exe_path.stat().st_size / 1024 / 1024
    print(f"✅ Executable created: {exe_size:.1f} MB")
    
    # Step 6: Create distribution package
    if not run_command("python create_package.py", "Creating distribution package"):
        print("❌ Failed to create distribution package")
        sys.exit(1)
    
    # Step 7: Show final results
    print("\n" + "=" * 60)
    print("🎉 BUILD COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    
    # Find the ZIP file
    zip_files = list(Path(".").glob("BlackzAllocator_v*.zip"))
    if zip_files:
        zip_file = zip_files[0]
        zip_size = zip_file.stat().st_size / 1024 / 1024
        print(f"\n📦 Distribution Package: {zip_file.name}")
        print(f"📏 Package Size: {zip_size:.1f} MB")
        print(f"📍 Location: {zip_file.absolute()}")
    
    print(f"\n📁 Files for distribution:")
    print(f"   • {zip_file.name} - Complete installer package")
    print(f"   • dist/BlackzAllocator.exe - Standalone executable")
    
    print(f"\n🚀 Instructions for your friend:")
    print(f"1. Send them the {zip_file.name} file")
    print(f"2. They extract it and run install.bat")
    print(f"3. Or they can run BlackzAllocator.exe directly")
    
    # Optional: Test the executable
    test = input("\n🧪 Test the executable now? (y/N): ").strip()
    if test.lower() == 'y':
        print("\n🚀 Launching BlackzAllocator...")
        try:
            subprocess.Popen([str(exe_path)], cwd=str(exe_path.parent))
            print("✅ BlackzAllocator launched successfully!")
            print("   Check if the GUI opens and connects to the API")
        except Exception as e:
            print(f"❌ Failed to launch: {e}")
    
    print("\n🎯 Build process complete!")
    print("Your BlackzAllocator is ready for distribution!")

if __name__ == "__main__":
    main() 