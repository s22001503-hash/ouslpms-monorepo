# Add Auto-Move Monitor to Windows Startup
# This runs automatically when you log in (no admin required)

Write-Host "`n=== SETTING UP AUTO-START (USER STARTUP) ===" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Join-Path $PSScriptRoot "auto_move_monitor.ps1"
$startupFolder = [System.Environment]::GetFolderPath('Startup')
$shortcutPath = Join-Path $startupFolder "OUSL_AutoMove_Monitor.lnk"

# Create WScript Shell object
$WshShell = New-Object -ComObject WScript.Shell

# Create shortcut
$Shortcut = $WshShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = "powershell.exe"
$Shortcut.Arguments = "-ExecutionPolicy Bypass -WindowStyle Hidden -File `"$scriptPath`""
$Shortcut.WorkingDirectory = $PSScriptRoot
$Shortcut.Description = "OUSL Auto-Move Monitor"
$Shortcut.Save()

Write-Host "✅ SUCCESS!" -ForegroundColor Green
Write-Host ""
Write-Host "Auto-Move Monitor added to Startup folder!" -ForegroundColor Cyan
Write-Host "Location: $shortcutPath" -ForegroundColor Gray
Write-Host ""
Write-Host "It will now:" -ForegroundColor Cyan
Write-Host "  ✅ Start automatically when you log in to Windows" -ForegroundColor Green
Write-Host "  ✅ Run in background (hidden window)" -ForegroundColor Green
Write-Host "  ✅ Monitor Downloads/Desktop/Documents" -ForegroundColor Green
Write-Host ""
Write-Host "Want to start it now without restarting?" -ForegroundColor Yellow
Write-Host "  Run: .\start_auto_move.bat" -ForegroundColor White
Write-Host ""
Write-Host "To disable auto-start:" -ForegroundColor Yellow
Write-Host "  Delete: $shortcutPath" -ForegroundColor White
Write-Host ""
