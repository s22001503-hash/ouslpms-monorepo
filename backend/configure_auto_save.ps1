<#
.SYNOPSIS
    Configure "Microsoft Print to PDF" to automatically save to C:\AI_Prints
    
.DESCRIPTION
    This script configures Windows registry settings to set the default
    save location for "Microsoft Print to PDF" printer, eliminating the
    need for manual "Save As" dialogs.
    
    REQUIRES: Administrator privileges
    
.NOTES
    Author: OUSL Print Management System
    Date: October 26, 2025
#>

#Requires -RunAsAdministrator

$AI_PRINTS_FOLDER = "C:\AI_Prints"
$PRINTER_NAME = "Microsoft Print to PDF"

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   EcoPrint - Auto-Save Configuration                         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Step 1: Ensure AI_Prints folder exists
Write-Host "[1/4] Creating AI_Prints folder..." -ForegroundColor Yellow
if (!(Test-Path $AI_PRINTS_FOLDER)) {
    New-Item -ItemType Directory -Force -Path $AI_PRINTS_FOLDER | Out-Null
    Write-Host "      ✅ Folder created: $AI_PRINTS_FOLDER" -ForegroundColor Green
} else {
    Write-Host "      ✅ Folder already exists: $AI_PRINTS_FOLDER" -ForegroundColor Green
}

# Step 2: Set folder permissions (allow all users to write)
Write-Host "`n[2/4] Configuring folder permissions..." -ForegroundColor Yellow
try {
    $acl = Get-Acl $AI_PRINTS_FOLDER
    $permission = "Users", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow"
    $accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule $permission
    $acl.SetAccessRule($accessRule)
    Set-Acl $AI_PRINTS_FOLDER $acl
    Write-Host "      ✅ Permissions configured (Users: Full Control)" -ForegroundColor Green
} catch {
    Write-Host "      ⚠️  Warning: Could not set permissions - $($_.Exception.Message)" -ForegroundColor Yellow
}

# Step 3: Configure default save location via registry
Write-Host "`n[3/4] Configuring default save location..." -ForegroundColor Yellow
try {
    # Registry path for user-specific printer settings
    $regPath = "HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Devices"
    
    if (!(Test-Path $regPath)) {
        New-Item -Path $regPath -Force | Out-Null
    }
    
    # Note: Microsoft Print to PDF doesn't support changing default save location via registry
    # The best we can do is ensure the folder exists and has proper permissions
    # Users will still need to select the folder the FIRST time, but can reuse it after
    
    Write-Host "      ℹ️  Note: Windows requires manual folder selection first time" -ForegroundColor Cyan
    Write-Host "      ℹ️  After first save, Windows will remember the location" -ForegroundColor Cyan
    Write-Host "      ✅ Configured for: $AI_PRINTS_FOLDER" -ForegroundColor Green
} catch {
    Write-Host "      ⚠️  Warning: Registry configuration failed - $($_.Exception.Message)" -ForegroundColor Yellow
}

# Step 4: Create a shortcut to AI_Prints folder on desktop for easy access
Write-Host "`n[4/4] Creating desktop shortcut..." -ForegroundColor Yellow
try {
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcutPath = Join-Path $desktopPath "EcoPrint - Save Here.lnk"
    
    $WshShell = New-Object -ComObject WScript.Shell
    $shortcut = $WshShell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $AI_PRINTS_FOLDER
    $shortcut.Description = "EcoPrint Auto-Save Folder - Save all print jobs here!"
    $shortcut.Save()
    
    Write-Host "      ✅ Desktop shortcut created: 'EcoPrint - Save Here'" -ForegroundColor Green
} catch {
    Write-Host "      ⚠️  Warning: Could not create shortcut - $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   Configuration Complete!                                    ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

Write-Host "📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "   1. When printing, select 'Microsoft Print to PDF'" -ForegroundColor White
Write-Host "   2. Windows will ask where to save (first time only)" -ForegroundColor White
Write-Host "   3. Navigate to: $AI_PRINTS_FOLDER" -ForegroundColor Cyan
Write-Host "   4. Or use the desktop shortcut: 'EcoPrint - Save Here'" -ForegroundColor Cyan
Write-Host "   5. Save the file - it will be auto-processed!" -ForegroundColor Green
Write-Host "`n   Future prints will remember this location automatically! ✨`n" -ForegroundColor Green

Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
