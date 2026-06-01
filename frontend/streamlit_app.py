from __future__ import annotations

import os
from pathlib import Path

import httpx
import streamlit as st

API_BASE = os.getenv("PAPERLENS_API_URL", "http://127.0.0.1:8000/api")

st.set_page_config(
    page_title="PaperLens",
    page_icon="🔬",
    layout="wide",
)


def _api_url(path: str) -> str:
    return f"{API_BASE.rstrip('/')}/{path.lstrip('/')}"


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------
def _init_state() -> None:
    if "analysis" not in st.session_state:
        st.session_state.analysis = None


_init_state()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.title("🔬 PaperLens")
st.sidebar.markdown("Analyse research papers with AI.")
st.sidebar.divider()

page = st.sidebar.radio("Navigation", ["Upload & Analyse", "Previous Papers"])

st.sidebar.divider()
st.sidebar.caption("PaperLens v0.1.0")


# ---------------------------------------------------------------------------
# Upload & Analyse page
# ---------------------------------------------------------------------------
def render_upload_page() -> None:
    st.header("Upload a Research Paper")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a research paper in PDF format (max 50 MB).",
    )

    if uploaded_file is None:
        st.info("Upload a PDF to get started.")
        # Show previous analysis if it exists
        if st.session_state.analysis:
            display_analysis(st.session_state.analysis)
        return

    # Validate size
    max_bytes = 50 * 1024 * 1024
    if len(uploaded_file.getvalue()) > max_bytes:
        st.error("File exceeds the 50 MB size limit.")
        return

    if st.button("Analyse Paper", type="primary"):
        with st.status("Processing…", expanded=True) as status:
            st.write("📄 Uploading file…")
            progress = st.progress(0, text="Uploading…")

            try:
                with httpx.Client(timeout=300) as client:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            "application/pdf",
                        )
                    }
                    resp = client.post(_api_url("/upload"), files=files)
                    resp.raise_for_status()
                    data = resp.json()
            except httpx.HTTPStatusError as exc:
                detail = "Unknown error"
                try:
                    detail = exc.response.json().get("detail", str(exc))
                except Exception:
                    detail = str(exc)
                st.error(f"Server error: {detail}")
                status.update(label="Failed", state="error")
                return
            except httpx.RequestError as exc:
                st.error(f"Could not reach the backend: {exc}")
                status.update(label="Failed", state="error")
                return

            progress.progress(50, text="Analysing with AI…")
            progress.progress(100, text="Done!")
            status.update(label="Analysis complete!", state="complete")

        st.session_state.analysis = data
        display_analysis(data)


# ---------------------------------------------------------------------------
# Display analysis results
# ---------------------------------------------------------------------------
def display_analysis(data: dict) -> None:
    st.divider()
    st.header(data.get("title", "Untitled"))

    if data.get("abstract"):
        with st.expander("Abstract", expanded=False):
            st.write(data["abstract"])

    s = data.get("summary", {})

    with st.expander("Executive Summary", expanded=True):
        st.write(s.get("executive_summary", ""))

    with st.expander("Key Findings", expanded=True):
        for finding in s.get("key_findings", []):
            st.markdown(f"- {finding}")

    with st.expander("Methodology", expanded=False):
        st.write(s.get("methodology", ""))

    with st.expander("Conclusion", expanded=False):
        st.write(s.get("conclusion", ""))

    with st.expander("Keywords", expanded=False):
        cols = st.columns(5)
        for i, kw in enumerate(s.get("keywords", [])):
            cols[i % 5].markdown(f"**{kw}**")

    with st.expander("Simple Explanation", expanded=True):
        st.write(data.get("simple_explanation", ""))

    # Download button
    report_path = data.get("report_path", "")
    if report_path:
        try:
            report_content = Path(report_path).read_text(encoding="utf-8")
            st.download_button(
                label="📥 Download Markdown Report",
                data=report_content,
                file_name=Path(report_path).name,
                mime="text/markdown",
            )
        except Exception:
            st.warning("Report file not available for download.")


# ---------------------------------------------------------------------------
# Previous papers page
# ---------------------------------------------------------------------------
def render_previous_papers() -> None:
    st.header("Previously Analysed Papers")

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(_api_url("/papers"))
            resp.raise_for_status()
            papers = resp.json()
    except httpx.RequestError:
        st.error("Could not reach the backend. Make sure PaperLens API is running.")
        return

    if not papers:
        st.info("No papers analysed yet.")
        return

    for p in papers:
        with st.container(border=True):
            cols = st.columns([3, 1, 1])
            cols[0].markdown(f"**{p['title']}**")
            cols[1].markdown(f"📄 {p['filename']}")
            cols[2].markdown(f"🗓 {p['upload_date'][:10]}")
            if st.button("View Details", key=f"view_{p['id']}"):
                with st.spinner("Fetching details…"):
                    try:
                        with httpx.Client(timeout=30) as client:
                            resp = client.get(_api_url(f"/papers/{p['id']}"))
                            resp.raise_for_status()
                            st.session_state.analysis = resp.json()
                    except httpx.RequestError:
                        st.error("Failed to fetch paper details.")
                st.rerun()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------
if page == "Upload & Analyse":
    render_upload_page()
else:
    render_previous_papers()
