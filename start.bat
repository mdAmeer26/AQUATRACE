@echo off
echo ========================================
echo    Starting AquaTrace Application
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Check if frontend node_modules exists
if not exist "frontend\node_modules" (
    echo [ERROR] Frontend dependencies not installed!
    echo Please run: cd frontend ; npm install
    pause
    exit /b 1
)

echo [1/2] Starting Backend API...
start "AquaTrace Backend" cmd /k ".venv\Scripts\activate && cd backend && python -m uvicorn api.main:app --reload"

REM Wait a moment for backend to initialize
timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend...
start "AquaTrace Frontend" cmd /k "cd frontend && npm start"

echo.
echo ========================================
echo    AquaTrace Started Successfully!
echo ========================================
echo.
echo Backend API: http://localhost:8000
echo Frontend:    http://localhost:3000
echo.
echo Press any key to stop all services...
pause > nul

echo.
echo Stopping services...
taskkill /FI "WindowTitle eq AquaTrace Backend*" /T /F > nul 2>&1
taskkill /FI "WindowTitle eq AquaTrace Frontend*" /T /F > nul 2>&1

echo Services stopped.
