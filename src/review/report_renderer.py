from __future__ import annotations

from src.review.schemas import RiskLevel, TradePlan


class ReportRenderer:
    def render(self, plan: TradePlan) -> str:
        lines = [
            f"# A股夜间复盘 {plan.trade_date}",
            "",
            f"- 市场观点：{plan.market_view}",
            f"- 风险等级：{self._risk_label(plan.risk_level)}",
            "",
            "## 市场摘要",
            "",
            plan.summary,
            "",
            "## 明日关注",
            "",
        ]

        if not plan.candidates:
            lines.append("今日不输出买入候选，优先观察。")
        else:
            for index, candidate in enumerate(plan.candidates, start=1):
                lines.extend(
                    [
                        f"### {index}. {candidate.code} {candidate.name}",
                        "",
                        f"- 类型：{candidate.style}",
                        f"- 理由：{candidate.reason}",
                        f"- 买入条件：{candidate.entry_condition}",
                        f"- 失效条件：{candidate.invalid_condition}",
                        f"- 止损：{candidate.stop_loss}",
                        f"- 止盈：{candidate.take_profit}",
                        f"- 仓位：{candidate.position_ratio:.0%}",
                        f"- 置信度：{candidate.confidence:.0%}",
                        f"- 风险：{'；'.join(candidate.risks) if candidate.risks else '未补充'}",
                        "",
                    ]
                )

        if plan.no_trade_conditions:
            lines.extend(["## 不交易条件", ""])
            lines.extend(f"- {item}" for item in plan.no_trade_conditions)
            lines.append("")

        lines.append("> 本报告仅用于个人复盘，不构成投资建议。")
        return "\n".join(lines)

    def _risk_label(self, risk_level: RiskLevel) -> str:
        labels = {
            RiskLevel.LOW: "低",
            RiskLevel.MEDIUM: "中",
            RiskLevel.HIGH: "高",
        }
        return labels[risk_level]

