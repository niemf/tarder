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
- [ ] Replace hard dependency on local AkShare data with a Doubao-led market context prompt covering A-shares, US equities, Japan/Korea markets, sector trends, major speeches/news, and price-hike clues.

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

- [x] Run one manual dry run without push.
- [x] Run one real Doubao review with PushPlus push.
- [ ] Run one manual dry run with Feishu fallback.
- [ ] Review 5 to 10 trading days of generated reports manually.

## 8. Current Status Notes

- [x] Configured local Doubao Ark REST endpoint and `doubao-seed-evolving` model in ignored local settings.
- [x] Configured local PushPlus token in ignored local settings.
- [x] Verified minimal Doubao API call returns successfully.
- [x] Verified full Doubao review flow completes and PushPlus returns `pushplus:ok`.
- [x] Restored corrupted Chinese prompt/report text and fixed report date to use the requested trade date.
- [ ] Next iteration: remove the weak AkShare-first assumption and let Doubao gather/analyze the day's market context directly from professional prompt requirements.
