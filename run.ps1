# SkillPath AI Launch Script for PowerShell
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Launching SkillPath AI (Unified Single App)...   " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan

# Check if frontend bundle exists; if not, build it once
if (-not (Test-Path "$root\skillpath-ai\frontend\dist\index.html")) {
    Write-Host "[Setup] Building frontend production bundle for unified serving..." -ForegroundColor Yellow
    Push-Location "$root\skillpath-ai\frontend"
    npm install
    npm run build
    Pop-Location
}

# Start backend which serves both frontend UI and FastAPI endpoints on http://127.0.0.1:8000
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$root\skillpath-ai\backend'; .\.venv\Scripts\Activate.ps1; python -m uvicorn main:app --reload --port 8000"

Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:8000"

Write-Host "`nSkillPath AI is running on a single unified URL!" -ForegroundColor Green
Write-Host "Single Website Link:  http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Interactive API Docs: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
Write-Host "Health Check:         http://127.0.0.1:8000/api/health" -ForegroundColor Yellow
