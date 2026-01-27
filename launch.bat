@echo off
title Valorant Stats Scraper
set SCRIPT_NAME=ribscraper.py

:: 1. Check if the Python file actually exists
if not exist "%SCRIPT_NAME%" (
    echo [ERROR] Could not find %SCRIPT_NAME% in this folder.
    echo Please make sure this .bat file is in the same folder as your script.
    pause
    exit
)

:: 2. Run the script
echo Starting Scraper...
echo ---------------------------------------------------------
python "%SCRIPT_NAME%"

:: 3. Keep window open if the script finishes or crashes
echo ---------------------------------------------------------
echo Script has finished executing.
pause