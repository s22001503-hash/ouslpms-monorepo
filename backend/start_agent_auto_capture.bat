@echo off
REM ============================================================================
REM EcoPrint Virtual Printer Agent - Automatic Capture Mode
REM ============================================================================
REM
REM This script starts the complete EcoPrint system with AUTOMATIC CAPTURE:
REM   1. Configures auto-save folder and permissions
REM   2. Starts auto-move monitor (watches Downloads/Documents/Desktop)
REM   3. Starts virtual printer agent with auto-capture enabled
REM
REM NO MANUAL SAVING REQUIRED - Print jobs are automatically captured!
REM
REM Author: OUSL Print Management System
REM Date: October 26, 2025
REM ============================================================================

title EcoPrint - Auto-Capture System

echo.
echo ============================================================================
echo    EcoPrint Virtual Printer Agent - AUTO-CAPTURE MODE
echo ============================================================================
echo.
echo    Automatic print job capture - NO manual saving required!
echo.
echo ============================================================================
echo.

REM Change to backend directory
cd /d "%~dp0"

REM Check for Administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] Not running as Administrator
    echo           Some features may be limited
    echo.
    timeout /t 3 >nul
) else (
    echo [OK] Running with Administrator privileges
    echo.
)

REM Step 1: Configure auto-save folder
echo [1/3] Configuring auto-save folder...
echo.
powershell -ExecutionPolicy Bypass -File "configure_auto_save.ps1"

echo.
echo ============================================================================
echo.

REM Step 2: Start auto-move monitor in background
echo [2/3] Starting auto-move monitor...
echo       Watching: Downloads, Documents, Desktop
echo       Auto-moving PDFs to: C:\AI_Prints
echo.
start "EcoPrint Auto-Move Monitor" /MIN powershell -ExecutionPolicy Bypass -WindowStyle Minimized -File "auto_move_monitor.ps1"
echo       Started in background (minimized window)
echo.

timeout /t 2 >nul

REM Step 3: Start virtual printer agent
echo [3/3] Starting Virtual Printer Agent...
echo       Auto-capture: ENABLED
echo       Authentication: REQUIRED
echo.

REM Activate virtual environment and run agent
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
    echo.
    
    python virtual_printer_agent.py
    
) else (
    echo [ERROR] Virtual environment not found!
    echo        Please run: python -m venv .venv
    echo        Then: .venv\Scripts\pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM If agent stops, cleanup
echo.
echo ============================================================================
echo    Agent stopped
echo ============================================================================
echo.
pause
