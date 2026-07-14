@echo off
title AI Uniform System - Web Application
color 0A

echo.
echo ================================================
echo    🎓 AI Uniform System - Web Application
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
echo 🔍 Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Flask...
    pip install flask
)

python -c "import firebase_admin" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing Firebase Admin SDK...
    pip install firebase-admin
)

echo ✅ Dependencies ready
echo.

REM Start the web application
echo 🚀 Starting web application...
echo 📱 The application will open in your browser automatically
echo 🌐 Manual access: http://127.0.0.1:5000
echo.
echo 🔑 Demo Credentials:
echo    Username: guidance1
echo    Password: guidance123
echo.
echo ⏹️  Press Ctrl+C to stop the server
echo ================================================
echo.

python start_web_app.py

pause





