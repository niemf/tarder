# AStock Review Bot

Auto trading review tool for nightly A-share market analysis.

A spec-driven A-share nightly review assistant.

Initial scope:

- Shanghai/Shenzhen main-board common stocks only
- Generate one nightly review report at 21:30
- Recommend 1 to 3 candidates with entry, stop loss, take profit, position, and invalidation rules
- Use Doubao as the primary model, with an optional reviewer model
- Push reports through PushPlus and/or Feishu
- No automatic trading in v0.1

See `openspec/changes/astock-review-bot-v0.1/` for the active proposal.

## Local Run

Create a local config from the example:

```powershell
Copy-Item config/settings.example.yaml config/settings.yaml
```

Install dependencies:

```powershell
pip install -e .
```

Or install the config parser only:

```powershell
pip install pyyaml
```

Set API keys with environment variables or edit `config/settings.yaml` locally:

```powershell
$env:DOUBAO_API_KEY="your-doubao-key"
$env:DEEPSEEK_API_KEY="your-deepseek-key"
$env:PUSHPLUS_TOKEN="your-pushplus-token"
$env:FEISHU_WEBHOOK_URL="your-feishu-webhook"
```

Run a dry review without network LLM calls or push:

```powershell
D:\DownLoad\Miniconda3\envs\myenv\python.exe -m src.jobs.nightly_review --dry-run --no-push
```

Run with real LLM calls but skip push:

```powershell
D:\DownLoad\Miniconda3\envs\myenv\python.exe -m src.jobs.nightly_review --no-push
```

Run with push enabled:

```powershell
python -m src.jobs.nightly_review
```

Generated reports are saved to `data/reports/` and SQLite records are saved to `data/review_bot.sqlite3`.

## Config Secrets

`config/settings.yaml` is ignored by Git and is intended for local secrets.

You can write real values directly:

```yaml
llm:
  doubao:
    api_key: "your-doubao-api-key"
    endpoint: "your-doubao-endpoint"
    model: "your-doubao-model"
  deepseek:
    api_key: "your-deepseek-api-key"

push:
  pushplus:
    token: "your-pushplus-token"
```

Or keep environment-variable references:

```yaml
api_key: "${DEEPSEEK_API_KEY}"
token: "${PUSHPLUS_TOKEN}"
```

The app reads `config/settings.yaml` at startup through `PyYAML`.

## Provider Notes

DeepSeek defaults to `https://api.deepseek.com/chat/completions` with model `deepseek-chat`.

Doubao/Volcengine Ark must be configured in `config/settings.yaml` after the model endpoint and model id are created in the provider console. The current implementation uses the OpenAI-compatible REST chat completions API directly.

## Service Scripts

The project uses a local `.venv` at runtime, but the `.venv` directory is not committed. Python virtual environments are machine-specific, so each user should create dependencies locally through the startup script.

Start the scheduler:

```sh
sh scripts/start.sh
```

Start with sample data and no push:

```sh
sh scripts/start.sh --dry-run --no-push
```

Stop the scheduler:

```sh
sh scripts/stop.sh
```

Clean logs:

```sh
sh scripts/clean_logs.sh
```

Runtime logs:

- `logs/review_bot.log`: scheduler heartbeat and job result logs
- `logs/review_bot.out.log`: process stdout/stderr from the startup script

The scheduler keeps running in the background, prints a heartbeat every 5 minutes, and triggers the nightly review at the configured time in `config/settings.yaml`.

### Windows PowerShell Scripts

This Windows machine does not expose `sh` in the default PowerShell path. Use the PowerShell scripts on Windows:

Start the scheduler:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start.ps1
```

Start with sample data and no push:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\start.ps1 -DryRun -NoPush
```

Stop the scheduler:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\stop.ps1
```

Clean logs:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\clean_logs.ps1
```

The PowerShell startup script creates `.venv` if it does not exist, installs dependencies into `.venv`, then launches the scheduler with that local Python interpreter.
