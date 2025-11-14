# Quick Start Script for Construction Contract Management
# Run this script to start both backend and frontend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Construction Contract Management" -ForegroundColor Cyan
Write-Host "Starting Servers..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "Error: Please run this script from the project root directory" -ForegroundColor Red
    exit 1
}

# Check backend .env
if (-not (Test-Path "backend\.env")) {
    Write-Host "Warning: backend\.env not found" -ForegroundColor Yellow
    Write-Host "  Make sure SUPABASE_URL, SUPABASE_ANON_KEY, and OPENAI_API_KEY are set" -ForegroundColor Yellow
}

# Check frontend .env
if (-not (Test-Path "frontend\.env")) {
    Write-Host "Warning: frontend\.env not found" -ForegroundColor Yellow
    Write-Host "  Make sure VITE_SUPABASE_URL and VITE_SUPABASE_ANON_KEY are set" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Starting Backend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000"

Start-Sleep -Seconds 2

Write-Host "Starting Frontend Server..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Start-Sleep -Seconds 3

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Servers Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:  http://localhost:8000" -ForegroundColor Yellow
Write-Host "API Docs:     http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Frontend:     http://localhost:5173" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to open the frontend in your browser..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Start-Process "http://localhost:5173"

