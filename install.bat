@echo off
REM NWExX Stego Linker Installation Script for Windows

echo 🎯 Installing NWExX Stego Linker...
echo ==================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is required but not installed.
    echo Please install Python 3.9 or higher and try again.
    pause
    exit /b 1
)

echo ✅ Python detected

REM Install requirements
echo 📦 Installing dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully
) else (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo 🎉 Installation complete!
echo.
echo Usage:
echo   python stego_linker.py --interactive
echo   python stego_linker.py --help
echo.
echo For more information, see README.md
pause
