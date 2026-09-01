@echo off
TITLE Trade OS - Local Environment Launcher
echo ===================================================
echo     Launching Trade OS (Docker + Backend + Frontend)
echo ===================================================
cd /d "%~dp0"
python start_local.py
pause
