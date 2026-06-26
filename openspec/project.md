# Project: AStock Review Bot

## Context

Build a personal A-share nightly review assistant for Shanghai/Shenzhen main-board common stocks.

The first release generates research and trade plans only. It does not place real orders.

## Current Decisions

- Market: A-share Shanghai/Shenzhen main-board common stocks only.
- Review time: 21:30 Asia/Shanghai.
- Recommendation count: 1 to 3 stocks per trading day.
- Trading style: short-term hot themes and trend swing setups, with occasional pullback opportunities.
- Primary model: Doubao.
- Review model: DeepSeek.
- Push: PushPlus for personal WeChat first, Feishu as stable fallback.
- Runtime: Windows PC first, cloud server later.
- Storage: SQLite for v0.1.

## Non-goals

- No automatic trading in v0.1.
- No crypto trading in v0.1.
- No ChiNext, STAR Market, Beijing Stock Exchange, ETF, convertible bond, futures, HK stock, or US stock trading in v0.1.
- No personal WeChat protocol automation in v0.1.

