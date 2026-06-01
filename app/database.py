from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

from app.config import settings
from app.exceptions import PaperLensError
from app.models.paper import PaperRecord


class DatabaseError(PaperLensError):
    """Raised on database operation failures."""


class Database:
    """Thin wrapper around SQLite for paper records."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        path = Path(db_path) if db_path else settings.upload_path / "paperlens.db"

        # If the path is relative, anchor it to the project root
        if not path.is_absolute():
            path = Path.cwd() / path

        path.parent.mkdir(parents=True, exist_ok=True)
        self._path = str(path)
        self._init_schema()

    def _init_schema(self) -> None:
        with sqlite3.connect(self._path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS papers (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename        TEXT NOT NULL,
                    title           TEXT NOT NULL DEFAULT '',
                    upload_date     TEXT NOT NULL,
                    summary         TEXT NOT NULL DEFAULT '',
                    simple_explanation TEXT NOT NULL DEFAULT '',
                    keywords        TEXT NOT NULL DEFAULT '',
                    report_path     TEXT NOT NULL DEFAULT ''
                )
                """
            )

    def _row_to_record(self, row: tuple) -> PaperRecord:
        return PaperRecord(
            id=row[0],
            filename=row[1],
            title=row[2],
            upload_date=datetime.fromisoformat(row[3]),
            summary=row[4],
            simple_explanation=row[5],
            keywords=row[6],
            report_path=row[7],
        )

    def insert_paper(self, paper: PaperRecord) -> int:
        with sqlite3.connect(self._path) as conn:
            cur = conn.execute(
                """
                INSERT INTO papers (filename, title, upload_date, summary,
                                    simple_explanation, keywords, report_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    paper.filename,
                    paper.title,
                    paper.upload_date.isoformat(),
                    paper.summary,
                    paper.simple_explanation,
                    paper.keywords,
                    paper.report_path,
                ),
            )
            return cur.lastrowid  # type: ignore[return-value]

    def get_paper(self, paper_id: int) -> PaperRecord | None:
        with sqlite3.connect(self._path) as conn:
            row = conn.execute(
                "SELECT * FROM papers WHERE id = ?", (paper_id,)
            ).fetchone()
        return self._row_to_record(row) if row else None

    def list_papers(self) -> list[PaperRecord]:
        with sqlite3.connect(self._path) as conn:
            rows = conn.execute(
                "SELECT * FROM papers ORDER BY upload_date DESC"
            ).fetchall()
        return [self._row_to_record(r) for r in rows]
