#!/usr/bin/env python3
"""PaperLens — entry point.

Starts the FastAPI backend. The landing page at http://127.0.0.1:8000
is the primary interface — upload PDFs and view analyses directly.

The legacy Streamlit frontend can be launched with --legacy-ui.

Usage:
    python run.py            # starts API (default)
    python run.py --legacy-ui   # starts API + legacy Streamlit UI
    python run.py --api      # starts API only
    python run.py --ui       # starts legacy Streamlit UI only
"""

from __future__ import annotations

import argparse
import subprocess
import sys


def start_api() -> subprocess.Popen:
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "0.0.0.0",
            "--port",
            "8000",
            "--reload",
        ],
    )


def start_legacy_ui() -> subprocess.Popen:
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "frontend/streamlit_app.py",
            "--server.port",
            "8501",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="PaperLens — research paper analyser"
    )
    parser.add_argument(
        "--legacy-ui",
        action="store_true",
        help="Also launch the legacy Streamlit frontend on port 8501",
    )
    parser.add_argument("--api", action="store_true", help="Start API only")
    parser.add_argument("--ui", action="store_true", help="Start legacy Streamlit UI only")
    args = parser.parse_args()

    processes: list[subprocess.Popen] = []

    if args.ui:
        processes.append(start_legacy_ui())
    elif args.api:
        processes.append(start_api())
    else:
        processes.append(start_api())
        if args.legacy_ui:
            processes.append(start_legacy_ui())

    if not processes:
        processes.append(start_api())

    print("PaperLens API running at http://127.0.0.1:8000")
    print("Open in your browser to upload and analyse papers.")
    print("Press Ctrl+C to stop.")

    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\nShutting down\u2026")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()


if __name__ == "__main__":
    main()
