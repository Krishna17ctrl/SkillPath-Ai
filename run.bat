@echo off
setlocal
echo ===================================================
echo   Launching SkillPath AI (Unified Single App)...
echo ===================================================

if not exist "%~dp0skillpath-ai\frontend\dist\index.html" (
    echo [Setup] Building frontend production bundle for unified serving...
    cd /d "%~dp0skillpath-ai\frontend"
    call npm install
    call npm run build
    cd /d "%~dp0"
)

if not exist "%~dp0skillpath-ai\backend\.venv\Scripts\python.exe" (
    echo [Setup] Creating Python virtual environment...
    cd /d "%~dp0skillpath-ai\backend"
    python -m venv .venv
    call .venv\Scripts\activate.bat
    python -m pip install -r requirements.txt
    cd /d "%~dp0"
)

start "SkillPath AI - Unified Platform" cmd /k "cd /d "%~dp0skillpath-ai\backend" && .venv\Scripts\activate.bat && python -m uvicorn main:app --reload --port 8000"

timeout /t 2 /nobreak >nul
start http://127.0.0.1:8000

echo.
echo ===================================================
echo   SkillPath AI is live on a single unified URL!
echo.
echo   Single Website Link:  http://127.0.0.1:8000
echo   Interactive API Docs: http://127.0.0.1:8000/docs
echo   Health Check:         http://127.0.0.1:8000/api/health
echo ===================================================
