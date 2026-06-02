from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app


def _make_minimal_pdf(text_body: str = "Hello World") -> bytes:
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


client = TestClient(app)


def test_upload_rejects_non_pdf() -> None:
    resp = client.post("/api/upload", files={"file": ("test.txt", b"hello", "text/plain")})
    assert resp.status_code == 400
    assert "PDF" in resp.json()["detail"]


def test_upload_rejects_empty_pdf() -> None:
    resp = client.post("/api/upload", files={"file": ("empty.pdf", b"", "application/pdf")})
    assert resp.status_code == 422
    assert "empty" in resp.json()["detail"].lower()


def test_upload_pdf_pipeline_attempted() -> None:
    """Upload a valid PDF and verify the pipeline runs.

    Without API keys the AI analysis step will fail, but we can verify
    that parsing, validation, and the error response all work correctly.
    """
    pdf_bytes = _make_minimal_pdf(
        "A Test Paper Title\n"
        "Author One\n"
        "Abstract\n"
        "This is a test abstract.\n"
    )
    resp = client.post(
        "/api/upload",
        files={"file": ("test.pdf", pdf_bytes, "application/pdf")},
    )

    # The AI step will fail (no API key), so we expect a 400 with a clear message
    assert resp.status_code == 400
    detail = resp.json().get("detail", "")
    assert "OPENAI_API_KEY" in detail or "API_KEY" in detail.upper()


def test_landing_page_served() -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert "text/html" in resp.headers["content-type"]


def test_list_papers() -> None:
    resp = client.get("/api/papers")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
