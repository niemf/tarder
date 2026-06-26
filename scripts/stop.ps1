$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

$PidFile = "run/review_bot.pid"
if (-not (Test-Path $PidFile)) {
    Write-Output "AStock Review Bot is not running: missing $PidFile"
    exit 0
}

$BotPid = Get-Content $PidFile -ErrorAction SilentlyContinue
$Process = if ($BotPid) { Get-Process -Id $BotPid -ErrorAction SilentlyContinue } else { $null }

if ($Process) {
    Stop-Process -Id $BotPid -Force
    Write-Output "AStock Review Bot stopped. pid=$BotPid"
} else {
    Write-Output "AStock Review Bot process not found. pid=$BotPid"
}

Remove-Item $PidFile -Force -ErrorAction SilentlyContinue
