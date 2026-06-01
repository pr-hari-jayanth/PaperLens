from __future__ import annotations

from app.ai.base import AIProvider
from app.exceptions import AIServiceError

_KEYWORD_SYSTEM_PROMPT = """\
You are an expert at identifying key concepts in research papers.
Extract 5-10 important keywords or short phrases from the text.

Return them as a comma-separated list on a single line.
Do not include numbering, bullet points, or any other formatting."""


async def extract_keywords(provider: AIProvider, paper_text: str) -> list[str]:
    """Extract important keywords from a paper using the given AI provider."""
    truncated = paper_text[:20_000] if len(paper_text) > 20_000 else paper_text

    prompt = f"""Extract 5-10 important keywords from this research paper text:

--- TEXT START ---
{truncated}
--- TEXT END ---"""

    raw = await provider.generate(
        prompt=prompt,
        system_prompt=_KEYWORD_SYSTEM_PROMPT,
        max_tokens=200,
        temperature=0.3,
    )

    raw = raw.strip()
    if not raw:
        raise AIServiceError("Keyword extractor returned an empty response.")

    # Split on commas and clean up
    keywords = [kw.strip().strip(".").strip('"').strip("'") for kw in raw.split(",")]
    # Filter out any empty strings
    keywords = [kw for kw in keywords if kw]
    return keywords[:10]
