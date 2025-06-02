@echo off
title BlackzAllocator Super Simple Installer
color 0B

echo.
echo ===============================================
echo    BlackzAllocator Super Simple Installer
echo    Professional IP Pool Management System  
echo ===============================================
echo.

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo [INFO] Looking for BlackzAllocator.exe...
echo [DEBUG] Current directory: %CD%

REM Check if BlackzAllocator.exe exists in current directory
if exist "BlackzAllocator.exe" (
    echo [OK] Found BlackzAllocator.exe in current directory
    set "EXE_LOCATION=%CD%\BlackzAllocator.exe"
    goto :found
)

REM Check parent directory
if exist "..\BlackzAllocator.exe" (
    echo [OK] Found BlackzAllocator.exe in parent directory
    set "EXE_LOCATION=%CD%\..\BlackzAllocator.exe"
    goto :found
)

REM Check dist subdirectory
if exist "dist\BlackzAllocator.exe" (
    echo [OK] Found BlackzAllocator.exe in dist directory
    set "EXE_LOCATION=%CD%\dist\BlackzAllocator.exe"
    goto :found
)

REM Check parent dist directory
if exist "..\dist\BlackzAllocator.exe" (
    echo [OK] Found BlackzAllocator.exe in parent dist directory
    set "EXE_LOCATION=%CD%\..\dist\BlackzAllocator.exe"
    goto :found
)

echo [ERROR] BlackzAllocator.exe not found!
echo [INFO] Please make sure BlackzAllocator.exe is in one of these locations:
echo         - Same directory as this installer
echo         - Parent directory
echo         - dist\ subdirectory
echo         - ..\dist\ directory
echo.
echo [DEBUG] Current directory contents:
dir /b
pause
exit /b 1

:found
echo [OK] Found executable at: %EXE_LOCATION%
echo.

REM Set installation directory
set "INSTALL_DIR=%USERPROFILE%\AppData\Local\BlackzAllocator"
echo [INFO] Installation directory: %INSTALL_DIR%
echo.

REM Ask user if they want to change the installation directory
set /p "CUSTOM_DIR=Press Enter for default, or enter custom path: "
if not "%CUSTOM_DIR%"=="" set "INSTALL_DIR=%CUSTOM_DIR%"

echo [INFO] Installing to: %INSTALL_DIR%

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo [OK] Created installation directory
)

REM Copy the executable
copy "%EXE_LOCATION%" "%INSTALL_DIR%\BlackzAllocator.exe" >nul
if %errorlevel% equ 0 (
    echo [OK] Copied BlackzAllocator.exe
) else (
    echo [ERROR] Failed to copy BlackzAllocator.exe
    pause
    exit /b 1
)

REM Create desktop shortcut (simple batch file)
set "DESKTOP=%USERPROFILE%\Desktop"
if exist "%DESKTOP%" (
    echo @echo off > "%DESKTOP%\BlackzAllocator.bat"
    echo cd /d "%INSTALL_DIR%" >> "%DESKTOP%\BlackzAllocator.bat"
    echo start "" "BlackzAllocator.exe" >> "%DESKTOP%\BlackzAllocator.bat"
    echo [OK] Created desktop shortcut
) else (
    echo [WARNING] Desktop folder not found
)

REM Create a simple README
echo BlackzAllocator - Professional IP Pool Management > "%INSTALL_DIR%\README.txt"
echo ================================================== >> "%INSTALL_DIR%\README.txt"
echo. >> "%INSTALL_DIR%\README.txt"
echo Installation Complete! >> "%INSTALL_DIR%\README.txt"
echo. >> "%INSTALL_DIR%\README.txt"
echo To run BlackzAllocator: >> "%INSTALL_DIR%\README.txt"
echo 1. Double-click BlackzAllocator.exe >> "%INSTALL_DIR%\README.txt"
echo 2. Use the desktop shortcut >> "%INSTALL_DIR%\README.txt"
echo 3. Run from: %INSTALL_DIR% >> "%INSTALL_DIR%\README.txt"
echo. >> "%INSTALL_DIR%\README.txt"
echo Enjoy using BlackzAllocator! >> "%INSTALL_DIR%\README.txt"

echo [OK] Created README.txt

echo.
echo ===============================================
echo    Installation Complete!
echo ===============================================
echo.
echo BlackzAllocator installed to: %INSTALL_DIR%
echo.
echo You can now run BlackzAllocator from:
echo   - Desktop shortcut (BlackzAllocator.bat)
echo   - Directly: %INSTALL_DIR%\BlackzAllocator.exe
echo.

REM Ask if user wants to launch now
set /p "LAUNCH=Launch BlackzAllocator now? (Y/n): "
if /i "%LAUNCH%"=="n" goto :end
if /i "%LAUNCH%"=="no" goto :end

echo [INFO] Launching BlackzAllocator...
start "" "%INSTALL_DIR%\BlackzAllocator.exe"
echo [OK] BlackzAllocator launched!

:end
echo.
echo Thank you for choosing BlackzAllocator!
pause 