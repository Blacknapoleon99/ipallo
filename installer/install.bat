@echo off
title BlackzAllocator Installer
color 0B

echo.
echo ===============================================
echo    BlackzAllocator Professional Installer
echo    IP Pool Management System
echo ===============================================
echo.

echo [INFO] Starting installation...
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo [INFO] Please install Python from https://python.org
    echo [INFO] Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Run the installer
echo [INFO] Running installer...
python installer\install_blackz.py

echo.
echo [INFO] Installation process completed
pause 