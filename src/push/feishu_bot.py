from __future__ import annotations

import json
import urllib.error
import urllib.request


class FeishuBot:
    def __init__(self, webhook_url: str) -> None:
        self.webhook_url = webhook_url

    def send_markdown(self, title: str, content: str) -> None:
        if not self.webhook_url:
            raise ValueError("Feishu webhook URL is empty.")

        payload = {
            "msg_type": "interactive",
            "card": {
                "config": {"wide_screen_mode": True},
                "header": {"title": {"tag": "plain_text", "content": title}},
                "elements": [{"tag": "markdown", "content": content}],
            },
        }
        request = urllib.request.Request(
            self.webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Feishu request failed: HTTP {exc.code} {body}") from exc

        if data.get("StatusCode", data.get("code", 0)) not in (0, "0"):
            raise RuntimeError(f"Feishu send failed: {data}")
