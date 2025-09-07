@echo off
echo Starting CSV Search Engine Web App...
echo.

call venv\Scripts\activate
cd src
streamlit run app.py

pause
