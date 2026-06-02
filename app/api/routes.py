from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.ai.factory import get_provider
from app.config import settings
from app.database import Database
from app.exceptions import AIServiceError, ConfigError, PDFParsingError
from app.models.paper import PaperAnalysis, PaperRecord
from app.services.keyword_extractor import extract_keywords
from app.services.pdf_parser import parse_pdf
from app.services.report_generator import save_report
from app.services.summarizer import generate_simple_explanation, generate_summary

router = APIRouter()
db = Database()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)) -> dict:
    """Upload a PDF, extract text, analyse it, and persist the result."""
    # --- Validate file type ---
    if not (file.filename and file.filename.lower().endswith(".pdf")):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted.")

    # --- Read content ---
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    content = await file.read()
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {settings.max_upload_size_mb} MB limit.",
        )

    # --- Save uploaded file temporarily ---
    upload_path = settings.upload_path / file.filename
    upload_path.write_bytes(content)

    # --- Parse PDF ---
    try:
        extracted = parse_pdf(content)
    except PDFParsingError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    # --- Analyse with AI ---
    try:
        provider = get_provider()
    except ConfigError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Run summarisation, keyword extraction, and simple explanation concurrently
    # (the provider calls are async so we can gather them)
    import asyncio

    summary_task = generate_summary(provider, extracted.text)
    keywords_task = extract_keywords(provider, extracted.text)
    explanation_task = generate_simple_explanation(
        provider, extracted.text, extracted.metadata.title
    )

    try:
        summary, keywords, explanation = await asyncio.gather(
            summary_task, keywords_task, explanation_task
        )
    except (AIServiceError, ConfigError) as exc:
        raise HTTPException(status_code=502, detail=str(exc))

    # Build the full analysis
    analysis = PaperAnalysis(
        title=extracted.metadata.title,
        abstract=extracted.metadata.abstract,
        summary=summary,
        simple_explanation=explanation,
    )

    # --- Save report to disk ---
    report_path = save_report(analysis, file.filename)

    # --- Persist to database ---
    record = PaperRecord(
        filename=file.filename,
        title=analysis.title,
        upload_date=datetime.now(UTC),
        summary=analysis.summary.model_dump_json(),
        simple_explanation=analysis.simple_explanation,
        keywords=", ".join(analysis.summary.keywords),
        report_path=str(report_path),
    )
    paper_id = db.insert_paper(record)

    return {
        "id": paper_id,
        "title": analysis.title,
        "abstract": analysis.abstract,
        "summary": analysis.summary.model_dump(),
        "simple_explanation": analysis.simple_explanation,
        "report_path": str(report_path),
    }


@router.get("/papers")
async def list_papers() -> list[dict]:
    """Return all previously analysed papers (metadata only)."""
    papers = db.list_papers()
    return [
        {
            "id": p.id,
            "filename": p.filename,
            "title": p.title,
            "upload_date": p.upload_date.isoformat(),
            "keywords": p.keywords,
            "report_path": p.report_path,
        }
        for p in papers
    ]


@router.get("/papers/{paper_id}")
async def get_paper(paper_id: int) -> dict:
    """Return full details for a single paper."""
    record = db.get_paper(paper_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Paper not found.")

    return {
        "id": record.id,
        "filename": record.filename,
        "title": record.title,
        "upload_date": record.upload_date.isoformat(),
        "summary": json.loads(record.summary) if record.summary else {},
        "simple_explanation": record.simple_explanation,
        "keywords": record.keywords,
        "report_path": record.report_path,
    }


@router.get("/reports/{filename:path}")
async def download_report(filename: str) -> FileResponse:
    """Download a generated Markdown report."""
    file_path = Path(filename)
    if not file_path.is_absolute():
        file_path = settings.report_path / file_path

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Report not found.")

    return FileResponse(str(file_path), media_type="text/markdown")
