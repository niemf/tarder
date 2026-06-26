# Tasks: AStock Review Bot v0.1

## 1. Project Setup

- [x] Add initial project README.
- [x] Add Python project metadata.
- [x] Add example settings file.
- [x] Add package skeleton.

## 2. Data Collection

- [x] Implement AkShare-based main-board stock universe collector.
- [x] Implement daily market snapshot collector.
- [ ] Implement index and sector summary collector.
- [x] Implement news and macro context collector.
- [ ] Cache raw collected data per trade date.

## 3. LLM Review

- [x] Implement Doubao provider.
- [x] Implement DeepSeek provider.
- [x] Build prompt templates for initial review and review pass.
- [x] Parse model output into strict JSON.
- [x] Store prompts and raw model outputs.

## 4. Risk and Validation

- [x] Define initial trade-plan schema.
- [x] Add initial deterministic risk filter.
- [x] Validate allowed stock prefixes.
- [ ] Reject ST, delisting-risk, and new stocks.
- [ ] Add no-trade condition checks.

## 5. Report and Push

- [x] Render final Markdown report.
- [x] Implement PushPlus push channel.
- [x] Implement Feishu push channel.
- [x] Add fallback push behavior.
- [x] Store push logs.

## 6. Scheduling and Runtime

- [x] Implement nightly review job.
- [x] Add Windows Task Scheduler setup notes.
- [x] Add local run instructions.
- [ ] Add cloud deployment notes.

## 7. Validation

- [ ] Run one manual dry run without push.
- [ ] Run one manual dry run with PushPlus.
- [ ] Run one manual dry run with Feishu fallback.
- [ ] Review 5 to 10 trading days of generated reports manually.
