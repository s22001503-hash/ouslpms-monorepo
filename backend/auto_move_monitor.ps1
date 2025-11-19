<#
.SYNOPSIS
    Advanced Auto-Move Monitor for Print Jobs
    
.DESCRIPTION
    Monitors common save locations (Downloads, Documents, Desktop) and
    automatically moves PDF files to C:\AI_Prints for processing.
    
    This provides AUTOMATIC capture without requiring users to manually
    save to the correct folder!
    
.NOTES
    Author: OUSL Print Management System
    Date: October 26, 2025
#>

$AI_PRINTS_FOLDER = "C:\AI_Prints"
$CHECK_INTERVAL = 2  # seconds

# Common folders where users might save print jobs
$WATCH_FOLDERS = @(
    "$env:USERPROFILE\Downloads",
    "$env:USERPROFILE\Documents",
    "$env:USERPROFILE\Desktop"
)

# Ensure AI_Prints folder exists
New-Item -ItemType Directory -Force -Path $AI_PRINTS_FOLDER | Out-Null

Write-Host "`n╔══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   EcoPrint - Auto-Move Print Monitor                         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "🔍 Monitoring folders:" -ForegroundColor Yellow
foreach ($folder in $WATCH_FOLDERS) {
    Write-Host "   📁 $folder" -ForegroundColor Cyan
}
Write-Host "`n💾 Auto-moving PDFs to: $AI_PRINTS_FOLDER" -ForegroundColor Green
Write-Host "`n⚡ Monitor Status: ACTIVE" -ForegroundColor Green
Write-Host "   Press Ctrl+C to stop...`n" -ForegroundColor Gray

$processedFiles = @{}  # Track recently processed files to avoid duplicates
$fileCounter = 0

while ($true) {
    try {
        foreach ($watchFolder in $WATCH_FOLDERS) {
            if (!(Test-Path $watchFolder)) {
                continue
            }
            
            # Get PDF files created in the last 30 seconds
            $recentPDFs = Get-ChildItem -Path $watchFolder -Filter "*.pdf" -ErrorAction SilentlyContinue | 
                Where-Object { 
                    $_.LastWriteTime -gt (Get-Date).AddSeconds(-30) -and 
                    $_.DirectoryName -ne $AI_PRINTS_FOLDER 
                }
            
            foreach ($file in $recentPDFs) {
                # Skip if already processed
                $fileKey = "$($file.FullName)|$($file.Length)|$($file.LastWriteTime)"
                if ($processedFiles.ContainsKey($fileKey)) {
                    continue
                }
                
                # Wait a moment to ensure file is fully written
                Start-Sleep -Milliseconds 500
                
                # Check if file is still being written (size changing)
                try {
                    $initialSize = $file.Length
                    Start-Sleep -Milliseconds 300
                    $file.Refresh()
                    $finalSize = $file.Length
                    
                    if ($initialSize -ne $finalSize) {
                        # File still being written, skip for now
                        continue
                    }
                } catch {
                    # File might be locked, skip
                    continue
                }
                
                # Generate unique filename
                $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
                $fileCounter++
                $baseName = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
                $newFileName = "${baseName}_${timestamp}.pdf"
                $destination = Join-Path $AI_PRINTS_FOLDER $newFileName
                
                # Move file to AI_Prints folder
                try {
                    Move-Item -Path $file.FullName -Destination $destination -Force -ErrorAction Stop
                    
                    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ✅ AUTO-MOVED: $($file.Name)" -ForegroundColor Green
                    Write-Host "                  📁 From: $($file.DirectoryName)" -ForegroundColor Gray
                    Write-Host "                  💾 To: $newFileName" -ForegroundColor Cyan
                    
                    # Mark as processed
                    $processedFiles[$fileKey] = $true
                    
                } catch {
                    Write-Host "[$(Get-Date -Format 'HH:mm:ss')] ⚠️  SKIP: $($file.Name) - $($_.Exception.Message)" -ForegroundColor Yellow
                }
            }
        }
        
        # Clean up old processed file entries (older than 5 minutes)
        if ($processedFiles.Count -gt 100) {
            $processedFiles.Clear()
        }
        
        Start-Sleep -Seconds $CHECK_INTERVAL
        
    } catch {
        Write-Host "❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        Start-Sleep -Seconds 5
    }
}
