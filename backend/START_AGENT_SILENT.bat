@echo off
REM Start Virtual Printer Agent in the background (no console window)
cd /d "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"

REM Start agent minimized without pause
start "EcoPrint Agent" /MIN python virtual_printer_agent.py

REM Optional: Show notification that agent started
powershell -WindowStyle Hidden -Command "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('EcoPrint Virtual Printer Agent is now running in the background.', 'EcoPrint Agent Started', 'OK', 'Information')"

exit
