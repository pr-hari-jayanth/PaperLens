from __future__ import annotations

from typing import Any

from app.ai.base import AIProvider
from app.config import settings
from app.exceptions import AIServiceError


class OllamaProvider(AIProvider):
    def __init__(self) -> None:
        self._base_url = settings.ollama_base_url.rstrip("/")
        self._model = settings.ollama_model

    @property
    def name(self) -> str:
        return "ollama"

    async def is_available(self) -> bool:
        import httpx

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(f"{self._base_url}/api/tags", timeout=5)
            return resp.status_code == 200
        except Exception:
            return False

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 2000,
        temperature: float = 0.3,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        import httpx

        body: dict[str, Any] = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": temperature,
            },
        }

        if system_prompt:
            body["system"] = system_prompt

        # Ollama does not natively support JSON mode via API flags,
        # but we can hint in the prompt. The summarizer prompt already
        # requests JSON output when needed.

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self._base_url}/api/generate", json=body, timeout=120
                )
                resp.raise_for_status()
                data = resp.json()
        except Exception as exc:
            raise AIServiceError(f"Ollama call failed: {exc}") from exc

        result = data.get("response", "")
        if not result:
            raise AIServiceError("Ollama returned an empty response.")
        return result
