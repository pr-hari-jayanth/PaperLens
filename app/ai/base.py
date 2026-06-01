from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class AIProvider(ABC):
    """Abstract interface for LLM providers.

    Every provider (OpenAI, Gemini, Ollama, …) implements this contract
    so that the rest of the application never depends on a concrete SDK.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 2000,
        temperature: float = 0.3,
        response_format: dict[str, Any] | None = None,
    ) -> str:
        """Send a prompt to the LLM and return the text response.

        Args:
            prompt: The user / main prompt.
            system_prompt: Optional system-level instruction.
            max_tokens: Maximum tokens in the response.
            temperature: Sampling temperature (0 = deterministic).
            response_format: Optional structured output spec
                             (e.g. {"type": "json_object"} for OpenAI).

        Returns:
            The generated text.
        """
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name (e.g. 'openai', 'gemini')."""
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Check whether the provider is configured and reachable."""
        ...
