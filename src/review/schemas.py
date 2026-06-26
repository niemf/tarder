from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


ALLOWED_PREFIXES = ("600", "601", "603", "605", "000", "001", "002", "003")


@dataclass
class CandidateStock:
    code: str
    name: str
    style: str
    reason: str
    entry_condition: str
    invalid_condition: str
    stop_loss: str
    take_profit: str
    position_ratio: float
    confidence: float
    risks: list[str] = field(default_factory=list)


@dataclass
class TradePlan:
    trade_date: str
    market_view: str
    risk_level: RiskLevel
    summary: str
    candidates: list[CandidateStock] = field(default_factory=list)
    no_trade_conditions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TradePlan":
        candidates = [CandidateStock(**item) for item in data.get("candidates", [])]
        if len(candidates) > 3:
            candidates = candidates[:3]

        for candidate in candidates:
            if not candidate.code.startswith(ALLOWED_PREFIXES) or len(candidate.code) != 6:
                raise ValueError(f"Unsupported stock code: {candidate.code}")
            if not 0 <= float(candidate.position_ratio) <= 0.3:
                raise ValueError(f"Invalid position ratio for {candidate.code}")
            if not 0 <= float(candidate.confidence) <= 1:
                raise ValueError(f"Invalid confidence for {candidate.code}")

        return cls(
            trade_date=str(data["trade_date"]),
            market_view=str(data["market_view"]),
            risk_level=_parse_risk_level(data["risk_level"]),
            summary=str(data["summary"]),
            candidates=candidates,
            no_trade_conditions=[str(item) for item in data.get("no_trade_conditions", [])],
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["risk_level"] = self.risk_level.value
        return data



def _parse_risk_level(value: Any) -> RiskLevel:
    text = str(value)
    if text.startswith('RiskLevel.'):
        text = text.rsplit('.', 1)[-1].lower()
    return RiskLevel(text)

