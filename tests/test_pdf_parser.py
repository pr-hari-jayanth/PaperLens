from __future__ import annotations

import pytest

from app.exceptions import PDFParsingError
from app.services.pdf_parser import parse_pdf


def _make_minimal_pdf(text_body: str = "Hello World") -> bytes:
    """Create a minimal valid PDF with embedded text."""
    # A minimal PDF that PyMuPDF can open
    body = text_body.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n"
        b"<< /Type /Catalog /Pages 2 0 R >>\n"
        b"endobj\n"
        b"2 0 obj\n"
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
        b"endobj\n"
        b"3 0 obj\n"
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]\n"
        b"   /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>\n"
        b"endobj\n"
        b"4 0 obj\n"
        b"<< /Length 44 >>\n"
        b"stream\n"
        b"BT /F1 12 Tf 100 700 Td ("
        + body.encode() +
        b") Tj ET\n"
        b"endstream\n"
        b"endobj\n"
        b"5 0 obj\n"
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\n"
        b"endobj\n"
        b"xref\n"
        b"0 6\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"0000000266 00000 n \n"
        b"0000000384 00000 n \n"
        b"trailer\n"
        b"<< /Size 6 /Root 1 0 R >>\n"
        b"startxref\n"
        b"460\n"
        b"%%EOF\n"
    )


def test_parse_valid_pdf() -> None:
    content = _make_minimal_pdf()
    result = parse_pdf(content)
    assert result.text
    assert result.page_count == 1


def test_parse_empty_bytes() -> None:
    with pytest.raises(PDFParsingError, match="empty"):
        parse_pdf(b"")


def test_parse_corrupted_pdf() -> None:
    with pytest.raises(PDFParsingError):
        parse_pdf(b"not a pdf at all")


def test_title_extraction() -> None:
    pdf_text = (
        "A Novel Approach to Quantum Computing\n"
        "John Doe, Jane Smith\n"
        "Abstract\n"
        "This paper presents a novel approach…\n"
    )
    content = _make_minimal_pdf(pdf_text)
    result = parse_pdf(content)
    assert "Novel Approach" in result.metadata.title


def test_abstract_extraction() -> None:
    pdf_text = (
        "Some Title\n"
        "Author\n"
        "Abstract\n"
        "This paper explores the use of machine learning for healthcare.\n"
        "We show that deep learning models outperform traditional methods.\n"
        "\n"
        "1. Introduction\n"
    )
    content = _make_minimal_pdf(pdf_text)
    result = parse_pdf(content)
    assert "machine learning" in result.metadata.abstract
    assert "healthcare" in result.metadata.abstract


def test_clean_removes_page_numbers() -> None:
    pdf_text = (
        "Introduction\n"
        "Some content here.\n"
        "42\n"
        "More content.\n"
    )
    content = _make_minimal_pdf(pdf_text)
    result = parse_pdf(content)
    # The page number "42" on its own line should be removed
    lines = [line.strip() for line in result.text.split("\n") if line.strip()]
    assert "42" not in lines
