from __future__ import annotations

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from app.database import Database
from app.models.paper import PaperRecord


@pytest.fixture
def db() -> Database:
    with tempfile.TemporaryDirectory() as tmp:
        yield Database(db_path=Path(tmp) / "test.db")


def test_insert_and_retrieve(db: Database) -> None:
    record = PaperRecord(
        filename="paper.pdf",
        title="Test Title",
        upload_date=datetime(2025, 1, 1),
        summary='{"key": "value"}',
        simple_explanation="Simple explanation.",
        keywords="AI, ML",
        report_path="/tmp/report.md",
    )
    paper_id = db.insert_paper(record)
    assert paper_id is not None

    retrieved = db.get_paper(paper_id)
    assert retrieved is not None
    assert retrieved.filename == "paper.pdf"
    assert retrieved.title == "Test Title"
    assert retrieved.simple_explanation == "Simple explanation."
    assert retrieved.keywords == "AI, ML"


def test_get_nonexistent_returns_none(db: Database) -> None:
    assert db.get_paper(9999) is None


def test_list_papers_empty(db: Database) -> None:
    assert db.list_papers() == []


def test_list_papers_returns_all(db: Database) -> None:
    db.insert_paper(PaperRecord(filename="a.pdf", title="A"))
    db.insert_paper(PaperRecord(filename="b.pdf", title="B"))
    papers = db.list_papers()
    assert len(papers) == 2
    assert papers[0].title == "B"  # most recent first


def test_auto_generates_upload_date(db: Database) -> None:
    paper_id = db.insert_paper(PaperRecord(filename="test.pdf", title="Test"))
    retrieved = db.get_paper(paper_id)
    assert retrieved is not None
    assert retrieved.upload_date is not None
