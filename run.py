#!/usr/bin/env python3
"""PaperLens — entry point.

Starts both the FastAPI backend and the Streamlit frontend.

Usage:
    python run.py            # starts both
    python run.py --api      # starts API only
    python run.py --ui       # starts UI only
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


def start_ui() -> subprocess.Popen:
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
    parser = argparse.ArgumentParser(description="PaperLens — research paper analyser")
    parser.add_argument("--api", action="store_true", help="Start API only")
    parser.add_argument("--ui", action="store_true", help="Start UI only")
    args = parser.parse_args()

    api_only = args.api
    ui_only = args.ui

    processes: list[subprocess.Popen] = []

    if ui_only:
        processes.append(start_ui())
    elif api_only:
        processes.append(start_api())
    else:
        processes.append(start_api())
        processes.append(start_ui())

    print("PaperLens running — press Ctrl+C to stop.")
    try:
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\nShutting down…")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()


if __name__ == "__main__":
    main()
