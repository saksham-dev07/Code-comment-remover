@echo off
setlocal EnableDelayedExpansion

REM ============================================================
REM Set console title and initial color (Green text on Black background)
REM ============================================================
title Flask App Setup and Run
color 0A

REM ============================================================
REM Print header
REM ============================================================
echo ===============================================================
echo                 FLASK APP SETUP & RUN UTILITY                 
echo ===============================================================
echo.

REM ============================================================
REM 1. Check if Python is installed
REM ============================================================
echo [INFO] Checking if Python is installed...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed. Please install Python and try again.
    pause
    exit /b 1
)
echo [SUCCESS] Python is installed.
echo ---------------------------------------------------------------

REM ============================================================
REM 2. Set up the Python virtual environment
REM ============================================================
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created.
) else (
    echo [INFO] Virtual environment already exists.
)
echo ---------------------------------------------------------------

REM ============================================================
REM 3. Activate the Python virtual environment
REM ============================================================
echo [INFO] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment. Please verify that the 'venv' folder exists.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated.
echo ---------------------------------------------------------------

REM ============================================================
REM 4. Upgrade pip and install required packages
REM ============================================================
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo [ERROR] Failed to upgrade pip. Please check your Python and pip installation.
    pause
    exit /b 1
)
echo [SUCCESS] Pip upgraded.
echo.

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found. Please ensure it is present in the current directory.
    pause
    exit /b 1
) else (
    echo [INFO] Installing required packages from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install required packages. Check requirements.txt and your internet connection.
        pause
        exit /b 1
    )
    echo [SUCCESS] All required packages installed.
)
echo ---------------------------------------------------------------

REM ============================================================
REM 5. Start the Flask application and open it in the browser
REM ============================================================
if not exist "app.py" (
    echo [ERROR] Flask app file 'app.py' not found.
    pause
    exit /b 1
)

echo [INFO] Starting Flask app...
start "" /b cmd /c "python app.py"
if errorlevel 1 (
    echo [ERROR] Failed to start the Flask app. Please check 'app.py' for errors.
    pause
    exit /b 1
)

REM Give the Flask server a few seconds to start before opening the browser.
timeout /t 5 /nobreak >nul

echo [INFO] Opening Flask app in browser...
start "" "http://127.0.0.1:5000/"

echo.
echo ===============================================================
echo          Flask app is now running at http://127.0.0.1:5000/
echo ===============================================================
echo.
pause
