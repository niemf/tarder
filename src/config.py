from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


ENV_PATTERN = re.compile(r"^\$\{([A-Z0-9_]+)\}$")


@dataclass
class ScheduleSettings:
    nightly_review_time: str = "21:30"
    timezone: str = "Asia/Shanghai"


@dataclass
class UniverseSettings:
    markets: list[str] = field(default_factory=lambda: ["sh_main_board", "sz_main_board"])
    exclude_st: bool = True
    exclude_new_stock_days: int = 60
    max_candidates: int = 3


@dataclass
class ProviderSettings:
    api_key: str = ""
    endpoint: str = ""
    model: str = ""


@dataclass
class LLMSettings:
    primary: str = "doubao"
    reviewer: str = "deepseek"
    doubao: ProviderSettings = field(default_factory=ProviderSettings)
    deepseek: ProviderSettings = field(
        default_factory=lambda: ProviderSettings(
            endpoint="https://api.deepseek.com/chat/completions",
            model="deepseek-chat",
        )
    )


@dataclass
class PushPlusSettings:
    token: str = ""
    channel: str = "wechat"
    template: str = "markdown"


@dataclass
class FeishuSettings:
    webhook_url: str = ""


@dataclass
class PushSettings:
    primary: str = "pushplus"
    fallback: str = "feishu"
    pushplus: PushPlusSettings = field(default_factory=PushPlusSettings)
    feishu: FeishuSettings = field(default_factory=FeishuSettings)


@dataclass
class RiskSettings:
    max_position_ratio_per_stock: float = 0.3
    preferred_position_ratio_per_stock: float = 0.2
    high_open_limit_percent: float = 5
    reject_without_stop_loss: bool = True


@dataclass
class AppSettings:
    schedule: ScheduleSettings = field(default_factory=ScheduleSettings)
    universe: UniverseSettings = field(default_factory=UniverseSettings)
    llm: LLMSettings = field(default_factory=LLMSettings)
    push: PushSettings = field(default_factory=PushSettings)
    risk: RiskSettings = field(default_factory=RiskSettings)


def _expand_env(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _expand_env(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_expand_env(item) for item in value]
    if isinstance(value, str):
        match = ENV_PATTERN.match(value)
        if match:
            return os.getenv(match.group(1), "")
    return value


def load_settings(path: str | Path = "config/settings.yaml") -> AppSettings:
    settings_path = Path(path)
    if not settings_path.exists():
        example_path = settings_path.with_name("settings.example.yaml")
        settings_path = example_path if example_path.exists() else settings_path

    if not settings_path.exists():
        return AppSettings()

    with settings_path.open("r", encoding="utf-8") as file:
        content = file.read()
    raw = _expand_env(yaml.safe_load(content) or {})
    return _settings_from_dict(raw)


def _settings_from_dict(raw: dict[str, Any]) -> AppSettings:
    llm = raw.get("llm", {})
    push = raw.get("push", {})
    return AppSettings(
        schedule=ScheduleSettings(**raw.get("schedule", {})),
        universe=UniverseSettings(**raw.get("universe", {})),
        llm=LLMSettings(
            primary=llm.get("primary", "doubao"),
            reviewer=llm.get("reviewer", "deepseek"),
            doubao=ProviderSettings(**llm.get("doubao", {})),
            deepseek=ProviderSettings(**llm.get("deepseek", {})),
        ),
        push=PushSettings(
            primary=push.get("primary", "pushplus"),
            fallback=push.get("fallback", "feishu"),
            pushplus=PushPlusSettings(**push.get("pushplus", {})),
            feishu=FeishuSettings(**push.get("feishu", {})),
        ),
        risk=RiskSettings(**raw.get("risk", {})),
    )
