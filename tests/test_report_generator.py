from __future__ import annotations

from app.models.paper import PaperAnalysis, SummaryResult
from app.services.report_generator import generate_markdown


def _sample_analysis() -> PaperAnalysis:
    return PaperAnalysis(
        title="Test Paper",
        abstract="A short abstract.",
        summary=SummaryResult(
            executive_summary="This is the executive summary.",
            key_findings=["Finding A", "Finding B", "Finding C"],
            methodology="We used a transformer model.",
            conclusion="We conclude that…",
            keywords=["AI", "NLP", "Transformers"],
        ),
        simple_explanation="This paper is about…",
    )


def test_generate_markdown_contains_title() -> None:
    md = generate_markdown(_sample_analysis())
    assert "# Test Paper" in md


def test_generate_markdown_contains_sections() -> None:
    md = generate_markdown(_sample_analysis())
    assert "## Executive Summary" in md
    assert "## Key Findings" in md
    assert "## Methodology" in md
    assert "## Conclusion" in md
    assert "## Keywords" in md
    assert "## Simple Explanation" in md


def test_generate_markdown_contains_abstract() -> None:
    md = generate_markdown(_sample_analysis())
    assert "## Abstract" in md
    assert "A short abstract." in md


def test_generate_markdown_key_findings_as_bullets() -> None:
    md = generate_markdown(_sample_analysis())
    assert "- Finding A" in md
    assert "- Finding B" in md
    assert "- Finding C" in md


def test_generate_markdown_keywords_as_bullets() -> None:
    md = generate_markdown(_sample_analysis())
    assert "- AI" in md
    assert "- NLP" in md
    assert "- Transformers" in md
