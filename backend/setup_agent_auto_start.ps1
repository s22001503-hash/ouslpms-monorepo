# Setup Auto-Start for Virtual Printer Agent
# This creates a Windows Scheduled Task to run on boot

Write-Host "`n=== SETTING UP AGENT AUTO-START ===" -ForegroundColor Cyan
Write-Host ""

$agentPath = Join-Path $PSScriptRoot "virtual_printer_agent.py"
$pythonPath = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$taskName = "OUSL_Virtual_Printer_Agent"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create scheduled task action
$action = New-ScheduledTaskAction -Execute $pythonPath `
    -Argument "`"$agentPath`"" `
    -WorkingDirectory $PSScriptRoot

# Create trigger (at logon)
$trigger = New-ScheduledTaskTrigger -AtLogOn

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -RunLevel Highest

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1)

# Register the task
try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger $trigger `
        -Principal $principal `
        -Settings $settings `
        -Description "Virtual Printer Agent for OUSL Print Management System" | Out-Null
    
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Virtual Printer Agent will now:" -ForegroundColor Cyan
    Write-Host "  ✅ Start automatically when you log in to Windows" -ForegroundColor Green
    Write-Host "  ✅ Run in background" -ForegroundColor Green
    Write-Host "  ✅ Auto-restart if it crashes" -ForegroundColor Green
    Write-Host ""
    Write-Host "Combined with Auto-Move Monitor:" -ForegroundColor Yellow
    Write-Host "  BOTH will start automatically on login!" -ForegroundColor Green
    Write-Host "  No manual steps needed!" -ForegroundColor Green
    Write-Host ""
    
} catch {
    Write-Host "❌ Scheduled Task failed (need Administrator)" -ForegroundColor Red
    Write-Host ""
    Write-Host "Trying Startup Folder method instead..." -ForegroundColor Yellow
    Write-Host ""
    
    # Fallback: Add to Startup folder
    $startupFolder = [System.Environment]::GetFolderPath('Startup')
    $shortcutPath = Join-Path $startupFolder "OUSL_Virtual_Printer_Agent.lnk"
    
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $pythonPath
    $Shortcut.Arguments = "`"$agentPath`""
    $Shortcut.WorkingDirectory = $PSScriptRoot
    $Shortcut.Description = "OUSL Virtual Printer Agent"
    $Shortcut.Save()
    
    Write-Host "✅ SUCCESS (Startup Folder)!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Virtual Printer Agent added to Startup!" -ForegroundColor Cyan
    Write-Host "Location: $shortcutPath" -ForegroundColor Gray
    Write-Host ""
    Write-Host "It will start automatically when you log in." -ForegroundColor Green
    Write-Host ""
}
