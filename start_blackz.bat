@echo off
echo Starting BlackzAllocator...
echo.

echo Changing to project directory...
cd /d "C:\GitHub\ipallo"

echo Starting API server...
start "BlackzAllocator API Server" cmd /k "python api_server.py"

echo Waiting for API server to start...
timeout /t 5

echo Starting GUI...
python gui_main.py

pause 