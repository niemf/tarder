from __future__ import annotations

from src.review.schemas import RiskLevel, TradePlan


class RiskFilter:
    def apply(self, plan: TradePlan) -> TradePlan:
        if plan.risk_level == RiskLevel.HIGH:
            plan.candidates = []
            return plan

        candidates = [
            candidate
            for candidate in plan.candidates
            if candidate.stop_loss.strip() and candidate.position_ratio <= 0.3
        ]
        plan.candidates = candidates[:3]
        return plan
