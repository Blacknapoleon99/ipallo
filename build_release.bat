@echo off
title BlackzAllocator Build System
color 0A

echo.
echo ===============================================
echo    BlackzAllocator Build System
echo    Professional IP Pool Management
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

echo [INFO] Starting automated build process...
echo.

REM Run the build script
python build_release.py

echo.
echo [INFO] Build process completed
pause 