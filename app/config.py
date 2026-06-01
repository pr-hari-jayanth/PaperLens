from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # AI provider selection
    ai_provider: str = "openai"

    # OpenAI
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"

    # Google Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"

    # Paths
    upload_dir: str = "uploads"
    report_dir: str = "reports"
    database_url: str = "sqlite:///paperlens.db"

    # Limits
    max_upload_size_mb: int = 50

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)

    @property
    def report_path(self) -> Path:
        return Path(self.report_dir)


settings = Settings()
