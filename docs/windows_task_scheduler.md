# Windows Task Scheduler

Use this after `python -m src.jobs.nightly_review --dry-run --no-push` works locally.

## Create Task

1. Open Task Scheduler.
2. Choose `Create Basic Task`.
3. Name it `AStock Review Bot`.
4. Trigger: daily at `21:30`.
5. Action: start a program.

Program:

```text
python
```

Arguments:

```text
-m src.jobs.nightly_review
```

Start in:

```text
D:\MyProject\Trader
```

## Safer First Schedule

Before enabling real push and API calls, schedule:

```text
-m src.jobs.nightly_review --dry-run --no-push
```

Then check:

- `data/reports/`
- `data/review_bot.sqlite3`

## Notes

- API keys should be configured as user environment variables or in local `config/settings.yaml`.
- Do not put real API keys in Git-tracked example files.
- If the Windows machine sleeps at night, enable wake timers or use a cloud server later.

