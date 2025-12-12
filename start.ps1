# AquaTrace Startup Script for PowerShell
# Run this with: .\start.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Starting AquaTrace Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if backend venv exists
if (-not (Test-Path "backend\venv")) {
    Write-Host "[ERROR] Backend virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run: cd backend ; python -m venv venv" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if frontend node_modules exists
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[ERROR] Frontend dependencies not installed!" -ForegroundColor Red
    Write-Host "Please run: cd frontend ; npm install" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/2] Starting Backend API..." -ForegroundColor Green
$backendPath = Join-Path $PWD "backend"
$backend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; & '.\venv\Scripts\python.exe' -m uvicorn api.main:app --reload" -PassThru -WindowStyle Normal

Start-Sleep -Seconds 3

Write-Host "[2/2] Starting Frontend..." -ForegroundColor Green
$frontendPath = Join-Path $PWD "frontend"
$frontend = Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm start" -PassThru -WindowStyle Normal

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AquaTrace Started Successfully!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API: " -NoNewline; Write-Host "http://localhost:8000" -ForegroundColor Yellow
Write-Host "Frontend:    " -NoNewline; Write-Host "http://localhost:3000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop all services..." -ForegroundColor Gray
Write-Host ""

# Wait for Ctrl+C
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
}
finally {
    Write-Host ""
    Write-Host "Stopping services..." -ForegroundColor Yellow
    Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue
    Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue
    Write-Host "Services stopped." -ForegroundColor Green
}
