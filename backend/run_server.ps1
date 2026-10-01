$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ProjectRoot = Split-Path -Parent $ScriptDir

Set-Location $ProjectRoot

# Activate virtual environment
if (Test-Path ".\backend\venv\Scripts\Activate.ps1") {
    . ".\backend\venv\Scripts\Activate.ps1"
} else {
    Write-Warning "Virtual environment not found at .\backend\venv"
}

# Run Uvicorn server on all interfaces to allow LAN access
Write-Host "Starting FastAPI server on http://0.0.0.0:8000..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
