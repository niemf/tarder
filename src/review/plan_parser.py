from __future__ import annotations

import json
import re

from src.review.schemas import TradePlan


JSON_BLOCK_PATTERN = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)


class PlanParser:
    def parse(self, text: str) -> TradePlan:
        content = self._extract_json(text)
        data = json.loads(content)
        return TradePlan.from_dict(data)

    def _extract_json(self, text: str) -> str:
        stripped = text.strip()
        match = JSON_BLOCK_PATTERN.search(stripped)
        if match:
            return match.group(1).strip()

        start = stripped.find("{")
        end = stripped.rfind("}")
        if start >= 0 and end > start:
            return stripped[start : end + 1]
        return stripped
