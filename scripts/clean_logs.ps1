$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Get-ChildItem -Path "logs" -Filter "*.log" -File -ErrorAction SilentlyContinue | Remove-Item -Force
Write-Output "Log files deleted from logs/."
