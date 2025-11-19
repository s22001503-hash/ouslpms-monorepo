@echo off
echo.
echo ========================================
echo   AUTO-MOVE MONITOR STARTER
echo ========================================
echo.
echo This will start the Auto-Move Monitor
echo that watches for PDFs in:
echo   - Downloads
echo   - Desktop  
echo   - Documents
echo.
echo Files will automatically move to C:\AI_Prints
echo.
pause
echo.
echo Starting Auto-Move Monitor...
echo.

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -NoExit -Command "& { Write-Host '`n=== AUTO-MOVE MONITOR ACTIVE ===' -ForegroundColor Green; Write-Host ''; Write-Host 'Watching folders:' -ForegroundColor Cyan; Write-Host '  - Downloads' -ForegroundColor White; Write-Host '  - Desktop' -ForegroundColor White; Write-Host '  - Documents' -ForegroundColor White; Write-Host ''; Write-Host 'Files will auto-move to C:\AI_Prints within 2 seconds' -ForegroundColor Yellow; Write-Host ''; Write-Host 'Keep this window open!' -ForegroundColor Red; Write-Host ''; & '.\auto_move_monitor.ps1' }"
