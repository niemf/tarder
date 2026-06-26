from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from src.collectors.market_collector import MarketCollector
from src.collectors.news_collector import NewsCollector
from src.config import AppSettings, load_settings
from src.llm.openai_compatible import OpenAICompatibleProvider
from src.push.feishu_bot import FeishuBot
from src.push.pushplus_bot import PushPlusBot
from src.review.context_builder import ContextBuilder
from src.review.plan_parser import PlanParser
from src.review.prompt_builder import PromptBuilder
from src.review.report_renderer import ReportRenderer
from src.review.risk_filter import RiskFilter
from src.review.schemas import RiskLevel, TradePlan
from src.storage.db import ReviewStore


def main() -> None:
    parser = argparse.ArgumentParser(description="Run A-share nightly review.")
    parser.add_argument("--config", default="config/settings.yaml")
    parser.add_argument("--trade-date", default=date.today().isoformat())
    parser.add_argument("--dry-run", action="store_true", help="Use sample data and skip real LLM calls.")
    parser.add_argument("--no-push", action="store_true", help="Generate and store report without push.")
    args = parser.parse_args()

    settings = load_settings(args.config)
    report = run_nightly_review(
        settings=settings,
        trade_date=args.trade_date,
        dry_run=args.dry_run,
        no_push=args.no_push,
    )
    print(report)


def run_nightly_review(
    settings: AppSettings,
    trade_date: str,
    dry_run: bool = False,
    no_push: bool = False,
) -> str:
    market_collector = MarketCollector()
    market = market_collector.sample(trade_date) if dry_run else market_collector.collect(trade_date)
    news = NewsCollector().collect()
    context_json = ContextBuilder().build(market, news)

    prompt_builder = PromptBuilder()
    parser = PlanParser()

    if dry_run:
        generator_output = _sample_plan_json(trade_date)
        reviewer_output = generator_output
    else:
        generator = _build_provider(settings, settings.llm.primary)
        reviewer = _build_provider(settings, settings.llm.reviewer)
        generator_output = generator.chat(
            prompt_builder.GENERATOR_SYSTEM_PROMPT,
            prompt_builder.build_generator_prompt(context_json),
        )
        reviewed_prompt = prompt_builder.build_reviewer_prompt(generator_output)
        reviewer_output = reviewer.chat(prompt_builder.REVIEWER_SYSTEM_PROMPT, reviewed_prompt)

    plan = parser.parse(reviewer_output)
    plan = RiskFilter().apply(plan)
    report = ReportRenderer().render(plan)
    push_status = "skipped"

    if not no_push:
        push_status = _push_report(settings, title=f"A股夜间复盘 {trade_date}", content=report)

    ReviewStore().save_report(
        trade_date=trade_date,
        context_json=context_json,
        generator_output=generator_output,
        reviewer_output=reviewer_output,
        plan=plan.to_dict(),
        report_markdown=report,
        push_status=push_status,
    )

    report_path = Path("data/reports") / f"{trade_date}.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8-sig")
    return report


def _build_provider(settings: AppSettings, provider_name: str) -> OpenAICompatibleProvider:
    provider_settings = getattr(settings.llm, provider_name)
    return OpenAICompatibleProvider(
        api_key=provider_settings.api_key,
        endpoint=provider_settings.endpoint,
        model=provider_settings.model,
    )


def _push_report(settings: AppSettings, title: str, content: str) -> str:
    errors: list[str] = []

    if settings.push.primary == "pushplus":
        try:
            bot = PushPlusBot(
                token=settings.push.pushplus.token,
                channel=settings.push.pushplus.channel,
                template=settings.push.pushplus.template,
            )
            bot.send_markdown(title, content)
            return "pushplus:ok"
        except Exception as exc:
            errors.append(f"pushplus:{exc}")

    if settings.push.fallback == "feishu":
        try:
            FeishuBot(settings.push.feishu.webhook_url).send_markdown(title, content)
            return "feishu:ok"
        except Exception as exc:
            errors.append(f"feishu:{exc}")

    return "failed:" + " | ".join(errors)


def _sample_plan_json(trade_date: str) -> str:
    plan = TradePlan(
        trade_date=trade_date,
        market_view="震荡偏强",
        risk_level=RiskLevel.MEDIUM,
        summary="样例复盘：市场成交温和放大，主线集中在AI应用和高股息方向，适合轻仓观察。",
        candidates=[
            {
                "code": "600000",
                "name": "样例股票A",
                "style": "趋势波段",
                "reason": "放量站上短期均线，板块有一定共振。",
                "entry_condition": "次日不高开超过3%，回踩5日线附近企稳后再考虑。",
                "invalid_condition": "跌破前一交易日低点或板块明显走弱。",
                "stop_loss": "跌破10日线或亏损4%。",
                "take_profit": "上涨8%到12%分批止盈。",
                "position_ratio": 0.2,
                "confidence": 0.68,
                "risks": ["样例数据不可用于真实交易", "高开过多不追"],
            }
        ],
        no_trade_conditions=["候选股高开超过5%", "上证指数低开低走且成交额明显萎缩"],
    )
    return json.dumps(plan.to_dict(), ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
