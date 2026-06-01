from __future__ import annotations

import json

from app.ai.base import AIProvider
from app.exceptions import AIServiceError
from app.models.paper import SummaryResult

_SUMMARIZE_SYSTEM_PROMPT = """\
You are an expert research analyst. Your task is to read a research paper and
produce a concise, structured summary.

Respond **only** with valid JSON in the following format (no markdown fences):
{
  "executive_summary": "2-3 paragraph high-level overview",
  "key_findings": ["finding 1", "finding 2", "finding 3", "finding 4", "finding 5"],
  "methodology": "1-2 paragraph description of methods used",
  "conclusion": "1-2 paragraph summary of conclusions",
  "keywords": ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"]
}
"""

_SIMPLE_EXPLAIN_SYSTEM_PROMPT = """\
You are a patient tutor explaining a research paper to a motivated high-school
student. Follow these rules:
- Avoid jargon; define any necessary technical terms simply.
- Use real-world examples or analogies when possible.
- Maximum 300 words.
- Do not use markdown formatting — plain prose only.
"""


def _parse_summary_json(raw: str) -> SummaryResult:
    """Parse the JSON returned by the LLM into a SummaryResult."""
    # Strip any markdown fences the model might add
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        # Remove opening fence (possibly ```json)
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline:]
        # Remove closing fence
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].rstrip()

    cleaned = cleaned.strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise AIServiceError(
            f"Failed to parse summary JSON from LLM response: {exc}\nRaw: {raw[:500]}"
        ) from exc

    return SummaryResult(
        executive_summary=data.get("executive_summary", ""),
        key_findings=data.get("key_findings", []),
        methodology=data.get("methodology", ""),
        conclusion=data.get("conclusion", ""),
        keywords=data.get("keywords", []),
    )


async def generate_summary(provider: AIProvider, paper_text: str) -> SummaryResult:
    """Generate a structured summary using the given AI provider."""
    # Truncate very long papers to avoid token limits
    truncated = paper_text[:50_000] if len(paper_text) > 50_000 else paper_text

    prompt = f"""Here is the full text of a research paper. Please produce a structured summary.

--- PAPER TEXT START ---
{truncated}
--- PAPER TEXT END ---"""

    raw = await provider.generate(
        prompt=prompt,
        system_prompt=_SUMMARIZE_SYSTEM_PROMPT,
        max_tokens=3000,
        temperature=0.3,
        response_format={"type": "json_object"} if provider.name != "ollama" else None,
    )

    return _parse_summary_json(raw)


async def generate_simple_explanation(
    provider: AIProvider, paper_text: str, title: str
) -> str:
    """Generate a plain-language explanation suitable for a high-school student."""
    truncated = paper_text[:30_000] if len(paper_text) > 30_000 else paper_text

    prompt = f"""Research paper title: {title}

Here is the paper content:

--- PAPER TEXT START ---
{truncated}
--- PAPER TEXT END ---

Explain what this paper is about to a motivated high-school student."""

    explanation = await provider.generate(
        prompt=prompt,
        system_prompt=_SIMPLE_EXPLAIN_SYSTEM_PROMPT,
        max_tokens=500,
        temperature=0.5,
    )

    return explanation.strip()
