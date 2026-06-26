from __future__ import annotations

from typing import Protocol


class PushChannel(Protocol):
    def send_markdown(self, title: str, content: str) -> None:
        """Send a markdown message."""

