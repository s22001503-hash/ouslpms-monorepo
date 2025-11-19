@echo off
REM ============================================================================
REM Simple Print Test - Just print to C:\AI_Prints directly
REM ============================================================================

title EcoPrint - Simple Print Test

echo.
echo ============================================================================
echo    Simple Print Test
echo ============================================================================
echo.
echo This test verifies that the agent processes files in C:\AI_Prints
echo.
echo INSTRUCTIONS:
echo.
echo 1. Open Notepad (or any application)
echo.
echo 2. Type some text
echo.
echo 3. File -^> Print -^> Select "Microsoft Print to PDF"
echo.
echo 4. In the Save dialog, navigate to: C:\AI_Prints
echo.
echo 5. Save the file with any name
echo.
echo 6. Watch below for agent processing...
echo.
echo ============================================================================
echo.

REM Check if agent is running
echo Checking agent status...
powershell -Command "$agent = Get-Process python -ErrorAction SilentlyContinue | Where-Object { (Get-WmiObject Win32_Process -Filter \"ProcessId = $($_.Id)\").CommandLine -like '*virtual_printer_agent*' }; if ($agent) { Write-Host '  Agent is RUNNING (PID: ' -NoNewline -ForegroundColor Green; Write-Host $agent.Id -NoNewline -ForegroundColor Cyan; Write-Host ')' -ForegroundColor Green } else { Write-Host '  Agent is NOT RUNNING!' -ForegroundColor Red; Write-Host '  Please start the agent first!' -ForegroundColor Yellow }"

echo.
echo Monitoring agent logs (Ctrl+C to stop)...
echo ============================================================================
echo.

REM Tail the agent log file
powershell -Command "Get-Content 'C:\AI_Prints\agent.log' -Wait -Tail 20"
