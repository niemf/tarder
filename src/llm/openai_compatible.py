from __future__ import annotations

import json
import urllib.error
import urllib.request


class OpenAICompatibleProvider:
    def __init__(self, api_key: str, endpoint: str, model: str, timeout_seconds: float = 60) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.model = model
        self.timeout_seconds = timeout_seconds

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("LLM API key is empty.")
        if not self.endpoint:
            raise ValueError("LLM endpoint is empty.")
        if not self.model:
            raise ValueError("LLM model is empty.")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM request failed: HTTP {exc.code} {body}") from exc
        return str(data["choices"][0]["message"]["content"])
