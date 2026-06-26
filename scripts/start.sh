#!/usr/bin/env sh
set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT_DIR"

mkdir -p logs run

PID_FILE="run/review_bot.pid"
LOG_FILE="logs/review_bot.out.log"

find_venv_python() {
  if [ -x ".venv/Scripts/python.exe" ]; then
    echo ".venv/Scripts/python.exe"
    return 0
  fi
  if [ -x ".venv/bin/python.exe" ]; then
    echo ".venv/bin/python.exe"
    return 0
  fi
  if [ -x ".venv/bin/python" ]; then
    echo ".venv/bin/python"
    return 0
  fi
  return 1
}

if [ -f "$PID_FILE" ]; then
  OLD_PID="$(cat "$PID_FILE")"
  if kill -0 "$OLD_PID" 2>/dev/null; then
    echo "AStock Review Bot is already running. pid=$OLD_PID"
    exit 0
  fi
  rm -f "$PID_FILE"
fi

if ! PYTHON_BIN="$(find_venv_python)"; then
  echo "Creating local virtual environment: .venv"
  python -m venv .venv
  PYTHON_BIN="$(find_venv_python)"
fi

if ! "$PYTHON_BIN" -c "import yaml" >/dev/null 2>&1; then
  echo "Installing project dependencies into .venv"
  "$PYTHON_BIN" -m pip install --disable-pip-version-check -e .
fi

nohup "$PYTHON_BIN" -m src.jobs.scheduler "$@" >> "$LOG_FILE" 2>&1 &
echo $! > "$PID_FILE"
echo "AStock Review Bot started. pid=$(cat "$PID_FILE") log=$LOG_FILE"
