from __future__ import annotations

from typing import Protocol


class LLMProvider(Protocol):
    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """Return a model response as text."""

