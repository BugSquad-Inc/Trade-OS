# Trade OS - PowerShell 1-Click Launcher
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "    Launching Trade OS (Docker + Backend + Frontend)" -ForegroundColor Green
Write-Host "===================================================" -ForegroundColor Cyan
python start_local.py
