@echo off
cd /d "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
echo ========================================
echo   Starting Virtual Printer Agent
echo   Authentication: ENABLED
echo ========================================
echo.
.\.venv\Scripts\python.exe virtual_printer_agent.py
pause
