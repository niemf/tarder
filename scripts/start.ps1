param(
    [switch]$DryRun,
    [switch]$NoPush,
    [int]$HeartbeatSeconds = 300
)

$ErrorActionPreference = "Stop"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $Root

New-Item -ItemType Directory -Force -Path "logs", "run" | Out-Null

$PidFile = "run/review_bot.pid"
$OutLog = "logs/review_bot.out.log"
$ErrLog = "logs/review_bot.err.log"

if (Test-Path $PidFile) {
    $OldPid = Get-Content $PidFile -ErrorAction SilentlyContinue
    if ($OldPid -and (Get-Process -Id $OldPid -ErrorAction SilentlyContinue)) {
        Write-Output "AStock Review Bot is already running. pid=$OldPid"
        exit 0
    }
    Remove-Item $PidFile -Force
}

function Get-VenvPython {
    $candidates = @(
        ".venv\Scripts\python.exe",
        ".venv\bin\python.exe",
        ".venv\bin\python"
    )
    foreach ($candidate in $candidates) {
        if (Test-Path $candidate) {
            return (Resolve-Path $candidate).Path
        }
    }
    return $null
}

$Python = Get-VenvPython
if (-not $Python) {
    Write-Output "Creating local virtual environment: .venv"
    python -m venv .venv
    $Python = Get-VenvPython
}

$PreviousErrorActionPreference = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& $Python -c "import yaml" *> $null
$YamlCheckExitCode = $LASTEXITCODE
$ErrorActionPreference = $PreviousErrorActionPreference

if ($YamlCheckExitCode -ne 0) {
    Write-Output "Installing project dependencies into .venv"
    & $Python -m pip install --disable-pip-version-check -e .
    if ($LASTEXITCODE -ne 0) {
        throw "Dependency installation failed."
    }
}

$ArgsList = @("-m", "src.jobs.scheduler", "--heartbeat-seconds", "$HeartbeatSeconds")
if ($DryRun) { $ArgsList += "--dry-run" }
if ($NoPush) { $ArgsList += "--no-push" }

$Process = Start-Process `
    -FilePath $Python `
    -ArgumentList $ArgsList `
    -WorkingDirectory $Root `
    -RedirectStandardOutput $OutLog `
    -RedirectStandardError $ErrLog `
    -WindowStyle Hidden `
    -PassThru

Set-Content -Path $PidFile -Value $Process.Id -Encoding ASCII
Write-Output "AStock Review Bot started. pid=$($Process.Id) log=$OutLog err=$ErrLog"
