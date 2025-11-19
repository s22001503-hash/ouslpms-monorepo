# PowerShell Script to Create Windows Task Scheduler Entry
# Run this script as Administrator to set up automatic startup

param(
    [switch]$NonInteractive = $false
)

$TaskName = "EcoPrint Virtual Printer Agent"
$Description = "Automatically starts the EcoPrint print monitoring and classification agent"
$PythonPath = "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend\.venv\Scripts\python.exe"
$ScriptPath = "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend\virtual_printer_agent.py"
$WorkingDir = "C:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EcoPrint Agent - Task Scheduler Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

# Remove existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create the scheduled task action
$Action = New-ScheduledTaskAction `
    -Execute $PythonPath `
    -Argument "`"$ScriptPath`"" `
    -WorkingDirectory $WorkingDir

# Create trigger - Run at system startup
$TriggerStartup = New-ScheduledTaskTrigger -AtStartup

# Create trigger - Run when user logs in
$TriggerLogon = New-ScheduledTaskTrigger -AtLogOn

# Create settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable:$false `
    -ExecutionTimeLimit (New-TimeSpan -Hours 0) `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -RestartCount 3

# Create principal (run as current user with highest privileges)
$Principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType Interactive `
    -RunLevel Highest

# Register the task
Write-Host "Creating scheduled task: $TaskName" -ForegroundColor Green
Register-ScheduledTask `
    -TaskName $TaskName `
    -Description $Description `
    -Action $Action `
    -Trigger $TriggerStartup, $TriggerLogon `
    -Settings $Settings `
    -Principal $Principal `
    -Force

Write-Host ""
Write-Host "SUCCESS! Scheduled task created." -ForegroundColor Green
Write-Host ""
Write-Host "The agent will now start automatically:" -ForegroundColor Cyan
Write-Host "  - When Windows starts up" -ForegroundColor White
Write-Host "  - When you log in" -ForegroundColor White
Write-Host ""
Write-Host "To manage the task:" -ForegroundColor Yellow
Write-Host "  - Open Task Scheduler (taskschd.msc)" -ForegroundColor White
Write-Host "  - Look for: $TaskName" -ForegroundColor White
Write-Host ""
Write-Host "To start the agent now without rebooting, run:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName `"$TaskName`"" -ForegroundColor White
Write-Host ""

# Ask if user wants to start now (unless non-interactive)
if (-not $NonInteractive) {
    $startNow = Read-Host "Do you want to start the agent now? (Y/N)"
} else {
    $startNow = 'Y'
    Write-Host "Non-interactive mode: Starting agent automatically..." -ForegroundColor Yellow
}

if ($startNow -eq 'Y' -or $startNow -eq 'y') {
    Write-Host "Starting agent..." -ForegroundColor Green
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 2
    
    # Check if running
    $task = Get-ScheduledTask -TaskName $TaskName
    $taskInfo = Get-ScheduledTaskInfo -TaskName $TaskName
    
    Write-Host "Task Status: $($task.State)" -ForegroundColor Cyan
    Write-Host "Last Run: $($taskInfo.LastRunTime)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Agent is now running in the background!" -ForegroundColor Green
}

if (-not $NonInteractive) {
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
