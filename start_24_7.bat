@echo off
echo ========================================
echo    CSV Search Engine - 24/7 Server
echo ========================================
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Start the 24/7 server
echo Starting 24/7 server...
python start_server.py

pause
