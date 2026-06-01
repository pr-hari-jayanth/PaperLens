from __future__ import annotations

from typing import Any

from openai import AsyncOpenAI

from app.ai.base import AIProvider
from app.config import settings
from app.exceptions import AIServiceError, ConfigError


class OpenAIProvider(AIProvider):
    def __init__(self) -> None:
        api_key = settings.openai_api_key
        if not api_key:
            raise ConfigError("OPENAI_API_KEY is not set in .env or environment.")
        self._client = AsyncOpenAI(api_key=api_key)
        self._model = settings.openai_model

    @property
    def name(self) -> str:
        return "openai"

    async def is_available(self) -> bool:
        try:
            await self._client.models.retrieve(self._model)
            return True
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
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        kwargs: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if response_format:
            kwargs["response_format"] = response_format

        try:
            response = await self._client.chat.completions.create(**kwargs)
        except Exception as exc:
            raise AIServiceError(f"OpenAI call failed: {exc}") from exc

        content = response.choices[0].message.content
        if content is None:
            raise AIServiceError("OpenAI returned an empty response.")
        return content
