@echo off
SETLOCAL EnableDelayedExpansion

echo Checking environment...

:: 1. Python Check
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [+] Python is already installed. Skipping...
) else (
    echo [-] Python not found. Installing...
    powershell -Command "Invoke-WebRequest -Uri https://www.python.org/ftp/python/3.11.5/python-3.11.5-amd64.exe -OutFile python_installer.exe"
    start /wait python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python_installer.exe
    echo [!] Python installed. Please restart this .bat file.
    pause
    exit
)

:: 2. Library Check
echo [+] Checking/Installing Playwright library...
python -m pip install --upgrade pip >nul
pip install playwright
echo [+] Playwright library is installed.

:: 3. Browser Check
echo [+] Checking/Installing Chromium browser...
python -m playwright install chromium
echo [+] Chromium browser is installed.

echo.
echo =========================================================
echo Done! Everything is ready to go.
echo =========================================================
pause