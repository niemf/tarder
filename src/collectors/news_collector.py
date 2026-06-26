from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class NewsContext:
    headlines: list[str] = field(default_factory=list)
    macro_notes: list[str] = field(default_factory=list)


class NewsCollector:
    def collect(self) -> NewsContext:
        # v0.1 starts with a conservative placeholder. Real provider adapters can
        # be added without changing the review flow.
        return NewsContext(
            headlines=["请结合当日公开财经新闻、政策变化、行业热点进行复盘。"],
            macro_notes=["关注外围市场、人民币汇率、商品价格和重要央行表态。"],
        )

