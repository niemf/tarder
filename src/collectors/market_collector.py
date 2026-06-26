from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MarketSnapshot:
    trade_date: str
    summary: str
    indices: list[dict[str, Any]] = field(default_factory=list)
    top_movers: list[dict[str, Any]] = field(default_factory=list)
    universe_count: int = 0


class MarketCollector:
    """Collects A-share market data for nightly review."""

    MAIN_BOARD_PREFIXES = ("600", "601", "603", "605", "000", "001", "002", "003")

    def collect(self, trade_date: str) -> MarketSnapshot:
        try:
            return self._collect_with_akshare(trade_date)
        except Exception as exc:
            return MarketSnapshot(
                trade_date=trade_date,
                summary=f"行情采集失败，已进入降级模式：{exc}",
            )

    def sample(self, trade_date: str) -> MarketSnapshot:
        return MarketSnapshot(
            trade_date=trade_date,
            summary="样例市场：指数震荡，成交额温和放大，短线热点集中在AI应用和高股息方向。",
            indices=[
                {"name": "上证指数", "change_pct": 0.42},
                {"name": "深证成指", "change_pct": 0.18},
            ],
            top_movers=[
                {"code": "600000", "name": "样例股票A", "change_pct": 4.2},
                {"code": "000001", "name": "样例股票B", "change_pct": 2.7},
            ],
            universe_count=2,
        )

    def _collect_with_akshare(self, trade_date: str) -> MarketSnapshot:
        import akshare as ak  # type: ignore[import-not-found]

        spot = ak.stock_zh_a_spot_em()
        code_col = "代码"
        name_col = "名称"
        change_col = "涨跌幅"

        universe = spot[
            spot[code_col].astype(str).str.startswith(self.MAIN_BOARD_PREFIXES)
            & ~spot[name_col].astype(str).str.contains("ST", case=False, na=False)
        ].copy()

        top = universe.sort_values(by=change_col, ascending=False).head(20)
        top_movers = [
            {
                "code": str(row[code_col]),
                "name": str(row[name_col]),
                "change_pct": float(row[change_col]),
            }
            for _, row in top.iterrows()
        ]

        summary = (
            f"沪深主板普通股票池约 {len(universe)} 只；"
            f"涨幅居前样本：{', '.join(item['name'] for item in top_movers[:5])}。"
        )
        return MarketSnapshot(
            trade_date=trade_date,
            summary=summary,
            top_movers=top_movers,
            universe_count=len(universe),
        )
