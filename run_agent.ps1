$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Set-Location (Join-Path $ScriptDir "agent")

# Activate virtual environment
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . ".\venv\Scripts\Activate.ps1"
} else {
    Write-Warning "Virtual environment not found at .\venv"
}

Write-Host "Starting PREDATOR Agent..."
python agent.py --backend "http://127.0.0.1:8000" --interval 5
