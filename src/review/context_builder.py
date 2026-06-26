from __future__ import annotations

import json

from src.collectors.market_collector import MarketSnapshot
from src.collectors.news_collector import NewsContext


class ContextBuilder:
    def build(self, market: MarketSnapshot, news: NewsContext) -> str:
        payload = {
            "trade_date": market.trade_date,
            "market_summary": market.summary,
            "indices": market.indices,
            "top_movers": market.top_movers,
            "universe_count": market.universe_count,
            "headlines": news.headlines,
            "macro_notes": news.macro_notes,
            "scope": {
                "market": "A股沪深主板普通股票",
                "styles": ["短线热点", "趋势波段", "低吸反弹"],
                "max_candidates": 3,
                "excluded": ["ST", "*ST", "创业板", "科创板", "北交所", "ETF", "可转债"],
            },
        }
        return json.dumps(payload, ensure_ascii=False, indent=2)
