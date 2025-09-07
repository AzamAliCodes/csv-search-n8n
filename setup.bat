@echo off
echo Setting up CSV Search Engine...
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error creating virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call venv\Scripts\activate

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error installing dependencies.
    pause
    exit /b 1
)

echo Step 4: Building search index...
cd src
python build_index.py
if %errorlevel% neq 0 (
    echo Error building index.
    pause
    exit /b 1
)

echo.
echo ====================================
echo Setup complete! You can now:
echo.
echo 1. Run CLI search: 
echo    cd src ^&^& python search.py
echo.
echo 2. Run web app: 
echo    cd src ^&^& streamlit run app.py
echo ====================================
echo.
pause
