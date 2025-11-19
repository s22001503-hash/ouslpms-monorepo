# OUSL Print Management - SQLite API Server
# Startup Script
# ============================================

Write-Host ""
Write-Host "╔═══════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     OUSL Print Management - SQLite API Server Launcher        ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$BACKEND_DIR = "c:\Users\user\Desktop\OCT Project\ouslpms-monorepo\backend"
$QUEUE_DB = "C:\AI_Prints\job_queue.db"
$API_PORT = 8001
$API_KEY = "ousl-sqlite-api-key-2025"

# Change to backend directory
Write-Host "📁 Changing to backend directory..." -ForegroundColor Yellow
Set-Location $BACKEND_DIR
Write-Host "   Current directory: $(Get-Location)" -ForegroundColor Gray
Write-Host ""

# Check if database exists
Write-Host "💾 Checking SQLite database..." -ForegroundColor Yellow
if (Test-Path $QUEUE_DB) {
    $fileSize = (Get-Item $QUEUE_DB).Length
    $fileSizeKB = [math]::Round($fileSize / 1KB, 2)
    Write-Host "   ✅ Database found: $QUEUE_DB" -ForegroundColor Green
    Write-Host "   📊 Size: $fileSizeKB KB" -ForegroundColor Gray
} else {
    Write-Host "   ⚠️  Database not found: $QUEUE_DB" -ForegroundColor Yellow
    Write-Host "   💡 Database will be created when agent processes first print job" -ForegroundColor Gray
}
Write-Host ""

# Check if Python is available
Write-Host "🐍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python not found!" -ForegroundColor Red
    Write-Host "   Please install Python or add it to PATH" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Check if port is available
Write-Host "🔌 Checking port $API_PORT..." -ForegroundColor Yellow
$portInUse = Get-NetTCPConnection -LocalPort $API_PORT -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "   ⚠️  Port $API_PORT is already in use!" -ForegroundColor Red
    Write-Host "   Process using port:" -ForegroundColor Yellow
    $portInUse | ForEach-Object {
        $processId = $_.OwningProcess
        $process = Get-Process -Id $processId -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "      PID: $processId - $($process.ProcessName)" -ForegroundColor Gray
        }
    }
    Write-Host ""
    $continue = Read-Host "   Do you want to kill the process and continue? (y/n)"
    if ($continue -eq 'y') {
        $portInUse | ForEach-Object {
            $processId = $_.OwningProcess
            Write-Host "   Killing process $processId..." -ForegroundColor Yellow
            Stop-Process -Id $processId -Force
        }
        Write-Host "   ✅ Process killed" -ForegroundColor Green
    } else {
        Write-Host "   ❌ Startup cancelled" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ✅ Port $API_PORT is available" -ForegroundColor Green
}
Write-Host ""

# Display configuration
Write-Host "⚙️  Configuration:" -ForegroundColor Yellow
Write-Host "   📊 Database: $QUEUE_DB" -ForegroundColor Gray
Write-Host "   🔌 Port: $API_PORT" -ForegroundColor Gray
Write-Host "   🔑 API Key: $API_KEY" -ForegroundColor Gray
Write-Host ""

# Display test commands
Write-Host "🧪 Test Commands:" -ForegroundColor Yellow
Write-Host "   Health Check (no auth):" -ForegroundColor Gray
Write-Host "      Invoke-WebRequest -Uri 'http://localhost:$API_PORT/' | Select-Object -ExpandProperty Content" -ForegroundColor DarkGray
Write-Host ""
Write-Host "   Get Summary Stats (with auth):" -ForegroundColor Gray
Write-Host "      `$headers = @{ 'X-API-Key' = '$API_KEY' }" -ForegroundColor DarkGray
Write-Host "      Invoke-WebRequest -Uri 'http://localhost:$API_PORT/api/stats/summary' -Headers `$headers | Select-Object -ExpandProperty Content" -ForegroundColor DarkGray
Write-Host ""

# Ask to continue
Write-Host "Press ENTER to start the server (or Ctrl+C to cancel)..." -ForegroundColor Cyan
Read-Host

# Start the server
Write-Host ""
Write-Host "🚀 Starting SQLite API Server..." -ForegroundColor Green
Write-Host "   Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Run the server
python sqlite_api_server.py
