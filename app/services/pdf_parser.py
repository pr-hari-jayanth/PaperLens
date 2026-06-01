from __future__ import annotations

import re

import fitz  # PyMuPDF

from app.exceptions import PDFParsingError
from app.models.paper import ExtractedText, PaperMetadata

# Patterns that look like page numbers / running headers to strip
_PAGE_NUMBER_RE = re.compile(r"^\s*\d+\s*$", re.MULTILINE)
_HEADER_FOOTER_CANDIDATES = re.compile(
    r"^\s*(arxiv|journal of|proceedings of|ieee|acm|springer|elsevier)"
    r".*?(vol|no|pp|page)\s*\d+.*?$",
    re.IGNORECASE | re.MULTILINE,
)


def _clean_text(text: str) -> str:
    """Remove likely page numbers and repeated header/footer lines."""
    # Remove standalone page numbers
    text = _PAGE_NUMBER_RE.sub("", text)

    # Remove common header/footer patterns
    text = _HEADER_FOOTER_CANDIDATES.sub("", text)

    # Collapse multiple blank lines into one
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _extract_title(text: str) -> str:
    """Heuristic: the first non-empty, non-trivial line is the title."""
    for line in text.split("\n"):
        stripped = line.strip()
        # Skip very short lines, page numbers, URLs
        if len(stripped) < 10:
            continue
        if stripped.startswith(("http", "www", "arXiv", "DOI")):
            continue
        # A plausible title is usually the first substantial line
        return stripped
    return "Untitled"


def _extract_abstract(text: str) -> str:
    """Heuristic: grab the paragraph after the word 'Abstract'."""
    match = re.search(
        r"\b(?:Abstract|ABSTRACT)\s*\n*\s*(.+?)(?:\n\s*\n|\Z)",
        text,
        re.DOTALL,
    )
    if match:
        return match.group(1).strip()
    return ""


def parse_pdf(content: bytes) -> ExtractedText:
    """Parse a PDF from raw bytes and return extracted text + metadata.

    Raises:
        PDFParsingError: If the PDF is corrupted, empty, or unreadable.
    """
    if not content:
        raise PDFParsingError("PDF content is empty.")

    try:
        doc = fitz.open(stream=content, filetype="pdf")
    except Exception as exc:
        raise PDFParsingError(f"Failed to open PDF: {exc}") from exc

    page_count = doc.page_count
    if page_count == 0:
        doc.close()
        raise PDFParsingError("PDF has zero pages.")

    raw_text_parts: list[str] = []
    for page in doc:
        raw_text_parts.append(page.get_text())

    doc.close()

    full_text = _clean_text("\n".join(raw_text_parts))

    if not full_text:
        raise PDFParsingError("No extractable text found in PDF. It may be a scanned image.")

    title = _extract_title(full_text)
    abstract = _extract_abstract(full_text)

    return ExtractedText(
        text=full_text,
        metadata=PaperMetadata(title=title, abstract=abstract),
        page_count=page_count,
    )
