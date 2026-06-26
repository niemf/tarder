from __future__ import annotations

import argparse
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from src.config import load_settings
from src.jobs.nightly_review import run_nightly_review


def main() -> None:
    parser = argparse.ArgumentParser(description="Run AStock Review Bot scheduler.")
    parser.add_argument("--config", default="config/settings.yaml")
    parser.add_argument("--dry-run", action="store_true", help="Use sample data when the scheduled job runs.")
    parser.add_argument("--no-push", action="store_true", help="Do not push scheduled reports.")
    parser.add_argument("--heartbeat-seconds", type=int, default=300)
    args = parser.parse_args()

    Path("logs").mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler("logs/review_bot.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    settings = load_settings(args.config)
    timezone = ZoneInfo(settings.schedule.timezone)
    target_time = settings.schedule.nightly_review_time
    last_run_date: str | None = None
    last_heartbeat = 0.0

    logging.info("AStock Review Bot scheduler started. target_time=%s timezone=%s", target_time, settings.schedule.timezone)

    while True:
        now = datetime.now(timezone)
        now_date = now.date().isoformat()
        now_hm = now.strftime("%H:%M")

        if time.time() - last_heartbeat >= args.heartbeat_seconds:
            logging.info("heartbeat now=%s next_review_time=%s", now.strftime("%Y-%m-%d %H:%M:%S"), target_time)
            last_heartbeat = time.time()

        if now_hm == target_time and last_run_date != now_date:
            logging.info("nightly review started trade_date=%s dry_run=%s no_push=%s", now_date, args.dry_run, args.no_push)
            try:
                run_nightly_review(settings=settings, trade_date=now_date, dry_run=args.dry_run, no_push=args.no_push)
                last_run_date = now_date
                logging.info("nightly review finished trade_date=%s", now_date)
            except Exception:
                logging.exception("nightly review failed trade_date=%s", now_date)

        time.sleep(30)


if __name__ == "__main__":
    main()
