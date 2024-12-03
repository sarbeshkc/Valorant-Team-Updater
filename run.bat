@echo off
setlocal

:: Colors for Windows console
set "GREEN=[32m"
set "BLUE=[34m"
set "RED=[31m"
set "NC=[0m"

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%Python is not installed. Please install Python and try again.%NC%
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo %BLUE%Creating virtual environment...%NC%
    python -m venv venv
    if errorlevel 1 (
        echo %RED%Failed to create virtual environment.%NC%
        exit /b 1
    )
)

:: Activate virtual environment
call venv\Scripts\activate
if errorlevel 1 (
    echo %RED%Failed to activate virtual environment.%NC%
    exit /b 1
)

:: Check if this is first run
if not exist venv\INSTALLED (
    echo %BLUE%First run detected. Running setup...%NC%
    python setup.py
    type nul > venv\INSTALLED
)

:: Run the updater
echo %GREEN%Starting overlay updater...%NC%
python app/updater.py

:: Deactivate virtual environment
deactivate

endlocal
