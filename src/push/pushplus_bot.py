from __future__ import annotations

import json
import urllib.error
import urllib.request


class PushPlusBot:
    ENDPOINT = "https://www.pushplus.plus/send"

    def __init__(self, token: str, channel: str = "wechat", template: str = "markdown") -> None:
        self.token = token
        self.channel = channel
        self.template = template

    def send_markdown(self, title: str, content: str) -> None:
        if not self.token:
            raise ValueError("PushPlus token is empty.")

        payload = {
            "token": self.token,
            "title": title,
            "content": content,
            "template": self.template,
            "channel": self.channel,
        }
        request = urllib.request.Request(
            self.ENDPOINT,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"PushPlus request failed: HTTP {exc.code} {body}") from exc

        if data.get("code") != 200:
            raise RuntimeError(f"PushPlus send failed: {data}")
