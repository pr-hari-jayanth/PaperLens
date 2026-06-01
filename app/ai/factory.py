from __future__ import annotations

from app.ai.base import AIProvider
from app.ai.providers.gemini import GeminiProvider
from app.ai.providers.ollama import OllamaProvider
from app.ai.providers.openai import OpenAIProvider
from app.config import settings
from app.exceptions import ConfigError

_PROVIDER_MAP: dict[str, type[AIProvider]] = {
    "openai": OpenAIProvider,
    "gemini": GeminiProvider,
    "ollama": OllamaProvider,
}


def get_provider(name: str | None = None) -> AIProvider:
    """Return an AI provider instance based on *name* (defaults to config)."""
    key = (name or settings.ai_provider).lower()

    cls = _PROVIDER_MAP.get(key)
    if cls is None:
        raise ConfigError(
            f"Unknown AI provider '{key}'. "
            f"Available: {', '.join(sorted(_PROVIDER_MAP))}"
        )
    return cls()
