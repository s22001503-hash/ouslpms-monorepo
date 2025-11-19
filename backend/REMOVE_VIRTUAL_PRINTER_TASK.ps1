# Remove Virtual Printer Scheduled Tasks - Run as ADMINISTRATOR

Write-Host "=== Virtual Printer Cleanup Script ===" -ForegroundColor Cyan
Write-Host ""

# Stop Python processes
Write-Host "Stopping Python processes..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -like "*python*"} | ForEach-Object {
    Write-Host "  Stopping: $($_.ProcessName) (PID: $($_.Id))" -ForegroundColor Gray
    Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue
}
Write-Host "Python processes stopped" -ForegroundColor Green
Write-Host ""

# Tasks to remove
$tasks = @(
    "EcoPrint Virtual Printer Agent",
    "EduPrintProv",
    "PrinterCleanupTask",
    "PrintJobCleanupTask"
)

# Remove scheduled tasks
Write-Host "Removing scheduled tasks..." -ForegroundColor Yellow
foreach ($taskName in $tasks) {
    $task = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
    if ($task) {
        Stop-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
        Write-Host "  Removed: $taskName" -ForegroundColor Green
    } else {
        Write-Host "  Not found: $taskName" -ForegroundColor Gray
    }
}
Write-Host ""

# Verify
Write-Host "Verifying cleanup..." -ForegroundColor Yellow
$remaining = Get-ScheduledTask | Where-Object {$_.TaskName -like "*print*" -or $_.TaskName -like "*OUSL*" -or $_.TaskName -like "*Eco*"}
if ($remaining) {
    Write-Host "  Remaining tasks:" -ForegroundColor Yellow
    $remaining | Select-Object TaskName, State | Format-Table
} else {
    Write-Host "  No print-related tasks found" -ForegroundColor Green
}

$pythonProcs = Get-Process | Where-Object {$_.ProcessName -like "*python*"}
if ($pythonProcs) {
    Write-Host "  Warning: Python processes running:" -ForegroundColor Yellow
    $pythonProcs | Select-Object ProcessName, Id | Format-Table
} else {
    Write-Host "  No Python processes running" -ForegroundColor Green
}

Write-Host ""
Write-Host "=== Cleanup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
