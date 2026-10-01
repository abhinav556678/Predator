$ErrorActionPreference = 'Stop'
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Set-Location (Join-Path $ScriptDir "frontend")

Write-Host "Starting Frontend on http://localhost:5173..."
npm run dev -- --host
