from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router

LANDING_DIR = Path(__file__).resolve().parent.parent / "frontend" / "landing" / "dist"


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.config import settings

    # Ensure required directories exist
    settings.upload_path.mkdir(parents=True, exist_ok=True)
    settings.report_path.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="PaperLens",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if LANDING_DIR.is_dir():
    app.mount("/", StaticFiles(directory=str(LANDING_DIR), html=True), name="landing")
