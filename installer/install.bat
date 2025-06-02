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
echo [DEBUG] Current directory: %CD%
echo [DEBUG] Batch file location: %~dp0
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

REM Change to the directory where this batch file is located
cd /d "%~dp0"
echo [DEBUG] Changed to directory: %CD%

REM Check if the installer Python script exists
if exist "installer\install_blackz.py" (
    echo [INFO] Found installer script at: installer\install_blackz.py
    python installer\install_blackz.py
) else if exist "install_blackz.py" (
    echo [INFO] Found installer script at: install_blackz.py
    python install_blackz.py
) else (
    echo [ERROR] Could not find installer script!
    echo [DEBUG] Looking for:
    echo          - installer\install_blackz.py
    echo          - install_blackz.py
    echo [DEBUG] Current directory contents:
    dir /b
    pause
    exit /b 1
)

echo.
echo [INFO] Installation process completed
pause 