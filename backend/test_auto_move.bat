@echo off
REM ============================================================================
REM Quick Test - Auto-Move Monitor
REM ============================================================================

title EcoPrint - Auto-Move Test

echo.
echo ============================================================================
echo    Quick Test: Auto-Move Monitor
echo ============================================================================
echo.

cd /d "%~dp0"

echo [Step 1/4] Creating test PDF in Downloads folder...
echo.

REM Create a test PDF file in Downloads
echo Test PDF Content - %date% %time% > "%USERPROFILE%\Downloads\ecoprint_test_%RANDOM%.txt"
echo    Created test file in Downloads
echo.

timeout /t 2 /nobreak >nul

echo [Step 2/4] Starting Auto-Move Monitor...
echo    Opening in new window...
echo.

REM Start monitor in new window
start "Auto-Move Monitor" powershell -ExecutionPolicy Bypass -NoExit -Command "& { Write-Host ''; Write-Host '=== Auto-Move Monitor ACTIVE ===' -ForegroundColor Green; Write-Host ''; Write-Host 'Watching:' -ForegroundColor Yellow; Write-Host '  Downloads' -ForegroundColor Cyan; Write-Host '  Documents' -ForegroundColor Cyan; Write-Host '  Desktop' -ForegroundColor Cyan; Write-Host ''; Write-Host 'Auto-moving PDFs to: C:\AI_Prints' -ForegroundColor Green; Write-Host ''; Write-Host 'Press Ctrl+C to stop' -ForegroundColor Gray; Write-Host ''; & '.\auto_move_monitor.ps1' }"

timeout /t 3 /nobreak >nul

echo [Step 3/4] Creating a PDF to test auto-move...
echo    Save any PDF to Downloads folder to see it auto-move!
echo.

echo [Step 4/4] Instructions:
echo.
echo    1. Open Notepad
echo    2. Type some text
echo    3. File -^> Print -^> Microsoft Print to PDF
echo    4. Save to Downloads folder
echo    5. Watch the Auto-Move Monitor window!
echo    6. File will auto-move to C:\AI_Prints
echo    7. Agent will process it automatically!
echo.

echo ============================================================================
echo.
echo Monitor is running in the background window.
echo Try printing something now!
echo.

pause
