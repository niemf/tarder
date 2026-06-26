from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class ReviewStore:
    def __init__(self, path: str | Path = "data/review_bot.sqlite3") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def save_report(
        self,
        trade_date: str,
        context_json: str,
        generator_output: str,
        reviewer_output: str,
        plan: dict[str, Any],
        report_markdown: str,
        push_status: str,
    ) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO review_reports (
                  trade_date, context_json, generator_output, reviewer_output,
                  plan_json, report_markdown, push_status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    trade_date,
                    context_json,
                    generator_output,
                    reviewer_output,
                    json.dumps(plan, ensure_ascii=False),
                    report_markdown,
                    push_status,
                ),
            )

    def _init_schema(self) -> None:
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS review_reports (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  trade_date TEXT NOT NULL,
                  context_json TEXT NOT NULL,
                  generator_output TEXT NOT NULL,
                  reviewer_output TEXT NOT NULL,
                  plan_json TEXT NOT NULL,
                  report_markdown TEXT NOT NULL,
                  push_status TEXT NOT NULL,
                  created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

