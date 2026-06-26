from __future__ import annotations


class PromptBuilder:
    GENERATOR_SYSTEM_PROMPT = (
        "你是谨慎的A股复盘助手。只分析沪深主板普通股票，不推荐ST、创业板、"
        "科创板、北交所、ETF、可转债。输出必须是合法JSON，不要输出Markdown。"
    )

    REVIEWER_SYSTEM_PROMPT = (
        "你是交易计划风控审查员。你的任务是审查候选股票是否追高、逻辑空泛、"
        "缺少止损或执行条件不清晰。输出必须是修正后的合法JSON，不要输出Markdown。"
    )

    def build_generator_prompt(self, context_json: str) -> str:
        return f"""
请根据以下市场上下文，生成明日A股复盘交易计划。

要求：
1. 只输出1到3只沪深主板普通股票。
2. 每只股票必须有买入条件、失效条件、止损、止盈、仓位和风险说明。
3. 如果市场风险较高，可以不给候选股。
4. 单票仓位不得超过0.3，本金较小，优先控制回撤。
5. 输出字段必须符合以下JSON结构：

{{
  "trade_date": "YYYY-MM-DD",
  "market_view": "震荡偏强/震荡/偏弱/高风险",
  "risk_level": "low/medium/high",
  "summary": "市场复盘摘要",
  "candidates": [
    {{
      "code": "600000",
      "name": "股票名称",
      "style": "短线热点/趋势波段/低吸反弹",
      "reason": "推荐理由",
      "entry_condition": "买入触发条件",
      "invalid_condition": "计划失效条件",
      "stop_loss": "止损条件或价格",
      "take_profit": "止盈条件或价格",
      "position_ratio": 0.2,
      "confidence": 0.7,
      "risks": ["风险1", "风险2"]
    }}
  ],
  "no_trade_conditions": ["不交易条件1"]
}}

市场上下文：
{context_json}
""".strip()

    def build_reviewer_prompt(self, plan_json: str) -> str:
        return f"""
请审查以下A股交易计划，并输出修正后的同结构JSON。

审查重点：
1. 删除代码不属于沪深主板的候选。
2. 删除没有清晰止损的候选。
3. 删除只有概念口号、没有执行条件的候选。
4. 对高开追涨风险给出明确 no_trade_conditions。
5. 候选股最多保留3只。

原始计划：
{plan_json}
""".strip()

