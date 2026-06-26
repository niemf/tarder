# Proposal: AStock Review Bot v0.1

## Context

The user wants a personal nightly A-share review system that runs at 21:30, analyzes daily market context with LLMs, produces 1 to 3 actionable candidate stocks, and pushes the result to personal channels.

## Problem

Manual nightly review is time-consuming and inconsistent. Direct fully automated trading is too risky before the review process, data pipeline, and trade-plan format are stable.

## Proposal

Build a v0.1 system that:

- Collects A-share market, theme, news, and macro context after market close.
- Limits the universe to Shanghai/Shenzhen main-board common stocks.
- Uses Doubao to generate the initial review and trade plan.
- Uses DeepSeek to review the plan for weak logic, missing stop loss, excessive chasing, and unclear execution conditions.
- Applies deterministic risk filters.
- Generates a Markdown report.
- Pushes the report through PushPlus first and Feishu as fallback.
- Saves raw context, prompts, model outputs, and final reports locally.

## Push Channel Decision

Use PushPlus first for personal WeChat because it is straightforward for personal notification delivery and supports simple HTTP message sending. Use Feishu as fallback because webhook robots are stable and suitable for longer Markdown reports.

ServerChan is a reasonable alternative, but PushPlus is preferred for v0.1 because the integration shape is simple and better aligned with personal WeChat notification use.

## Non-goals

- No real-money trading.
- No broker integration.
- No intraday automated execution.
- No crypto trading.
- No direct personal WeChat client automation.

## Risks

- Public market/news data may be delayed or incomplete.
- LLM output may include hallucinated reasons or vague trade conditions.
- Chinese financial data sources can change response formats.
- Push providers may rate-limit or change API behavior.

## Mitigations

- Keep all LLM responses and prompts in logs.
- Require strict JSON schema validation before generating the final report.
- Use deterministic filters for stock universe, candidate count, stop loss, and position sizing.
- Support multiple push channels.

