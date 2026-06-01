from __future__ import annotations

from typing import Any

from app.ai.base import AIProvider
from app.config import settings
from app.exceptions import AIServiceError, ConfigError


class GeminiProvider(AIProvider):
    """Minimal Gemini provider via the HTTP API (no google-generativeai SDK)."""

    def __init__(self) -> None:
        self._api_key = settings.gemini_api_key
        if not self._api_key:
            raise ConfigError("GEMINI_API_KEY is not set in .env or environment.")
        self._model = settings.gemini_model
        self._base_url = "https://generativelanguage.googleapis.com/v1beta"

    @property
    def name(self) -> str:
        return "gemini"

    async def is_available(self) -> bool:
        import httpx

        url = f"{self._base_url}/models/{self._model}"
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params={"key": self._api_key})
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

        url = f"{self._base_url}/models/{self._model}:generateContent"

        contents: list[dict[str, Any]] = [{"parts": [{"text": prompt}]}]

        body: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
                "temperature": temperature,
            },
        }

        if system_prompt:
            body["systemInstruction"] = {"parts": [{"text": system_prompt}]}

        if response_format and response_format.get("type") == "json_object":
            body["generationConfig"]["responseMimeType"] = "application/json"

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    url, params={"key": self._api_key}, json=body, timeout=60
                )
                resp.raise_for_status()
                data = resp.json()
        except Exception as exc:
            raise AIServiceError(f"Gemini call failed: {exc}") from exc

        candidates = data.get("candidates", [])
        if not candidates:
            raise AIServiceError("Gemini returned no candidates.")

        text_parts = []
        for part in candidates[0].get("content", {}).get("parts", []):
            if "text" in part:
                text_parts.append(part["text"])

        result = "".join(text_parts)
        if not result:
            raise AIServiceError("Gemini returned an empty response.")
        return result
