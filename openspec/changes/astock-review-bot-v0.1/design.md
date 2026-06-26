# Design: AStock Review Bot v0.1

## Architecture

```text
config/
  settings.example.yaml
src/
  collectors/
    market_collector.py
    news_collector.py
    macro_collector.py
  llm/
    base.py
    doubao_provider.py
    deepseek_provider.py
  review/
    context_builder.py
    prompt_builder.py
    schemas.py
    risk_filter.py
    report_renderer.py
  push/
    base.py
    pushplus_bot.py
    feishu_bot.py
  storage/
    db.py
  jobs/
    nightly_review.py
```

## Flow

```text
21:30 scheduler
  -> collect market data
  -> collect news and macro context
  -> build normalized review context
  -> call Doubao for initial JSON trade plan
  -> call DeepSeek to review and revise risk issues
  -> validate JSON schema
  -> apply deterministic risk filters
  -> render Markdown report
  -> push through PushPlus
  -> fallback to Feishu if needed
  -> persist context, prompts, outputs, report, and push result
```

## Stock Universe

Allowed code prefixes:

- Shanghai main board: `600`, `601`, `603`, `605`
- Shenzhen main board: `000`, `001`, `002`, `003`

Excluded:

- ST and *ST
- Delisting-risk stocks
- Newly listed stocks within configured days
- ChiNext, STAR Market, Beijing Stock Exchange
- ETF, convertible bond, fund, futures

## Trade Plan Schema

The final plan must include:

- trade date
- market view
- risk level
- market summary
- 1 to 3 candidates
- no-trade conditions

Each candidate must include:

- code
- name
- style
- reason
- entry condition
- invalid condition
- stop loss
- take profit
- position ratio
- confidence
- risks

## Risk Rules

- Reject candidates without a clear stop loss.
- Reject candidates outside allowed code prefixes.
- Limit candidates to 3.
- Limit single-stock position ratio to 30%.
- If market risk is high, output observation only.
- Add no-trade conditions for high open, index weakness, and theme breakdown.

## Runtime

v0.1 runs on a Windows PC using either:

- manual command execution, or
- Windows Task Scheduler at 21:30.

The same code should later run on a cloud server with a cron or process supervisor.

