from __future__ import annotations


class PaperLensError(Exception):
    """Base exception for all PaperLens errors."""


class PDFParsingError(PaperLensError):
    """Raised when PDF extraction fails."""


class AIServiceError(PaperLensError):
    """Raised when an AI provider call fails."""


class ConfigError(PaperLensError):
    """Raised when configuration is invalid or missing."""
