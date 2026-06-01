from __future__ import annotations

from pathlib import Path

from app.config import settings
from app.models.paper import PaperAnalysis


def generate_markdown(analysis: PaperAnalysis) -> str:
    """Render the analysis as a Markdown string."""
    lines: list[str] = []

    lines.append(f"# {analysis.title}")
    lines.append("")

    if analysis.abstract:
        lines.append("## Abstract")
        lines.append("")
        lines.append(analysis.abstract)
        lines.append("")

    s = analysis.summary
    lines.append("## Executive Summary")
    lines.append("")
    lines.append(s.executive_summary)
    lines.append("")

    lines.append("## Key Findings")
    lines.append("")
    for finding in s.key_findings:
        lines.append(f"- {finding}")
    lines.append("")

    lines.append("## Methodology")
    lines.append("")
    lines.append(s.methodology)
    lines.append("")

    lines.append("## Conclusion")
    lines.append("")
    lines.append(s.conclusion)
    lines.append("")

    lines.append("## Keywords")
    lines.append("")
    for kw in s.keywords:
        lines.append(f"- {kw}")
    lines.append("")

    lines.append("## Simple Explanation")
    lines.append("")
    lines.append(analysis.simple_explanation)
    lines.append("")

    return "\n".join(lines)


def save_report(analysis: PaperAnalysis, filename: str) -> Path:
    """Write the Markdown report to disk and return the path."""
    out_dir = settings.report_path
    out_dir.mkdir(parents=True, exist_ok=True)

    safe_name = Path(filename).stem.replace(" ", "_")
    out_path = out_dir / f"{safe_name}_report.md"

    markdown = generate_markdown(analysis)
    out_path.write_text(markdown, encoding="utf-8")

    return out_path
