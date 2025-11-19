@echo off
REM One-Click Installer for EcoPrint Agent Auto-Startup
REM This batch file must be run as Administrator

echo ========================================
echo   EcoPrint Agent - Auto-Startup Setup
echo ========================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: This script must be run as Administrator!
    echo.
    echo Please right-click this file and select "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo [1/3] Setting up Task Scheduler...
powershell -ExecutionPolicy Bypass -File "%~dp0Install-AutoStartup.ps1" -NonInteractive

if %errorLevel% equ 0 (
    echo.
    echo [2/3] Verifying installation...
    powershell -Command "Get-ScheduledTask -TaskName 'EcoPrint Virtual Printer Agent' | Format-List State, LastRunTime"
    
    echo.
    echo [3/3] Starting agent...
    powershell -Command "Start-ScheduledTask -TaskName 'EcoPrint Virtual Printer Agent'"
    timeout /t 2 >nul
    
    echo.
    echo ========================================
    echo   SUCCESS! 
    echo ========================================
    echo.
    echo The EcoPrint Agent will now start automatically:
    echo   - When Windows starts
    echo   - When you log in
    echo.
    echo The agent is currently running in the background.
    echo.
) else (
    echo.
    echo ERROR: Installation failed!
    echo Please check the error messages above.
    echo.
)

pause
