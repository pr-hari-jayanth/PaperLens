from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router


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
