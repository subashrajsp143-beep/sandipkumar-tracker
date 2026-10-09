@echo off
title 19 Sites Material Consumption Tracker
echo ========================================================
echo   19 Sites Project Material Tracker - Starting...
echo ========================================================
echo.

cd /d "%~dp0"

echo Opening browser at http://127.0.0.1:5000 in 2 seconds...
start "" timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000

echo Starting Python server...
python app.py

pause
