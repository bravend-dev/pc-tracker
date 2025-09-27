@echo off
echo Building PCTracker Installer...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Install PyInstaller if not already installed
echo Installing/updating PyInstaller...
pip install pyinstaller

REM Run the build script
echo.
echo Starting build process...
cd /d "%~dp0.."
python scripts/build.py

echo.
echo Build process completed!
pause

