#!/usr/bin/env sh
set -eu

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
cd "$ROOT_DIR"

PID_FILE="run/review_bot.pid"

if [ ! -f "$PID_FILE" ]; then
  echo "AStock Review Bot is not running: missing $PID_FILE"
  exit 0
fi

PID="$(cat "$PID_FILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "AStock Review Bot stopped. pid=$PID"
else
  echo "AStock Review Bot process not found. pid=$PID"
fi

rm -f "$PID_FILE"
