from __future__ import annotations

import os
from pathlib import Path

import httpx
import streamlit as st

API_BASE = os.getenv("PAPERLENS_API_URL", "http://127.0.0.1:8000/api")

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="PaperLens",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom CSS
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* ── Base ── */
    .main > div { padding: 1.5rem 2rem; }
    .stAppHeader { background: transparent !important; }
    .stApp { background: #f8fafc; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        padding: 1rem 0;
    }
    section[data-testid="stSidebar"] .stApp {
        background: transparent !important;
    }
    section[data-testid="stSidebar"] .sidebar-title {
        color: #e2e8f0;
        font-size: 1.5rem;
        font-weight: 700;
        padding: 0 1.5rem 0.5rem;
        letter-spacing: -0.02em;
    }
    section[data-testid="stSidebar"] .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.85rem;
        padding: 0 1.5rem 1.5rem;
        border-bottom: 1px solid #334155;
        margin-bottom: 0.5rem;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label {
        color: #cbd5e1 !important;
        font-size: 0.95rem;
        padding: 0.5rem 1.5rem;
        border-radius: 0;
        border-left: 3px solid transparent;
        transition: all 0.15s;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label:hover {
        background: #1e293b;
        color: #f1f5f9 !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] [data-testid="stMarkdownContainer"] {
        font-size: 0.95rem;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] label[data-selected="true"] {
        background: #1e293b;
        color: #ffffff !important;
        border-left-color: #38bdf8;
        font-weight: 600;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadio"] input {
        display: none;
    }

    /* ── Cards ── */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .card-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.75rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f1f5f9;
    }

    /* ── Headers ── */
    h1, h2, h3 { color: #0f172a; }
    .page-title {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.25rem;
    }
    .page-desc {
        color: #64748b;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* ── Upload zone ── */
    .upload-zone {
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 3rem 2rem;
        text-align: center;
        background: #f8fafc;
        transition: all 0.2s;
    }
    .upload-zone:hover { border-color: #38bdf8; background: #f0f9ff; }
    .upload-zone .upload-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
    .upload-zone .upload-text { font-size: 1.05rem; color: #334155; font-weight: 500; }
    .upload-zone .upload-hint { font-size: 0.85rem; color: #94a3b8; margin-top: 0.25rem; }

    /* ── Status & alerts ── */
    .stAlert { border-radius: 8px; }
    .error-card {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 10px;
        padding: 1.25rem;
        margin: 1rem 0;
    }
    .error-card .error-title {
        color: #991b1b;
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    .error-card .error-body {
        color: #7f1d1d;
        font-size: 0.9rem;
    }
    .error-card .error-tip {
        background: #fee;
        padding: 0.75rem;
        border-radius: 6px;
        margin-top: 0.5rem;
        font-size: 0.85rem;
        color: #7f1d1d;
    }

    /* ── Metrics ── */
    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetric"] > div { color: #0f172a; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-weight: 600 !important;
        color: #0f172a !important;
        background: white !important;
        border-radius: 8px !important;
        border: 1px solid #e2e8f0 !important;
    }
    .streamlit-expanderHeader:hover { background: #f8fafc !important; }
    .streamlit-expanderContent {
        border: 1px solid #e2e8f0;
        border-top: none;
        border-radius: 0 0 8px 8px;
        padding: 1rem !important;
        background: white;
    }

    /* ── Button ── */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.15s;
    }
    .stButton > button[kind="primary"] {
        background: #2563eb;
        color: white;
        border: none;
    }
    .stButton > button[kind="primary"]:hover {
        background: #1d4ed8;
        box-shadow: 0 4px 12px rgba(37,99,235,0.3);
    }

    /* ── Spinner ── */
    .stSpinner > div { border-color: #2563eb !important; }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.8rem;
        padding: 2rem 0 0.5rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Error message helpers
# ---------------------------------------------------------------------------

def friendly_error(status_code: int, detail: str) -> dict:
    """Map a backend error to a user-friendly message + troubleshooting tip."""
    detail_lower = detail.lower()

    # ── 400 Bad Request ──
    if "only pdf" in detail_lower:
        return {
            "title": "Unsupported file type",
            "message": "PaperLens currently only accepts PDF files.",
            "tip": "Export your document as a PDF and try again.",
        }

    # ── 413 Payload Too Large ──
    if status_code == 413 or "exceeds" in detail_lower and "mb" in detail_lower:
        return {
            "title": "File too large",
            "message": detail,
            "tip": "Try splitting your PDF into smaller parts, or compress it with a tool like Adobe Acrobat or ilovepdf.com.",
        }

    # ── 422 PDF parsing errors ──
    if "empty" in detail_lower and "content" in detail_lower:
        return {
            "title": "Empty PDF",
            "message": "The PDF file appears to be empty.",
            "tip": "Check that the file is not corrupted and contains actual content.",
        }
    if "failed to open pdf" in detail_lower:
        return {
            "title": "Could not read PDF",
            "message": detail,
            "tip": "The file may be corrupted or password-protected. Try opening it in a PDF reader first.",
        }
    if "zero pages" in detail_lower:
        return {
            "title": "Empty PDF",
            "message": "The PDF has no pages.",
            "tip": "Make sure the PDF contains at least one page of content.",
        }
    if "no extractable text" in detail_lower or "scanned" in detail_lower:
        return {
            "title": "Scanned document detected",
            "message": "PaperLens could not extract text from the PDF. It may be a scanned image or contain only pictures.",
            "tip": "Try using an OCR tool (like OCR.space or Adobe Acrobat) to convert the scan to text, then upload again.",
        }

    # ── 404 Not Found ──
    if status_code == 404:
        return {
            "title": "Not found",
            "message": detail,
            "tip": "The requested paper or report could not be found. It may have been deleted.",
        }

    # ── 500 AI / config / database errors ──
    if "api_key" in detail_lower and "not set" in detail_lower:
        provider = "OpenAI" if "openai" in detail_lower else "Google Gemini" if "gemini" in detail_lower else "the AI provider"
        return {
            "title": "API key not configured",
            "message": f"The {provider} API key is missing.",
            "tip": "Open the `.env` file in the project root and add the required API key. Then restart the backend server.",
        }
    if "unknown ai provider" in detail_lower:
        return {
            "title": "Configuration error",
            "message": detail,
            "tip": "Check the `AI_PROVIDER` setting in your `.env` file. Valid options are: gemini, ollama, openai.",
        }
    if "call failed" in detail_lower:
        provider = (
            "OpenAI" if "openai" in detail_lower
            else "Google Gemini" if "gemini" in detail_lower
            else "Ollama" if "ollama" in detail_lower
            else "the AI"
        )
        return {
            "title": f"{provider} service error",
            "message": detail,
            "tip": (
                "This is usually a temporary network issue or an API outage. "
                "Check your internet connection, verify your API key is valid, and try again."
            ),
        }
    if "empty response" in detail_lower:
        return {
            "title": "AI returned an empty result",
            "message": "The AI model did not return any content.",
            "tip": "Try again — some models occasionally return empty results. If the problem persists, check the AI provider status.",
        }
    if "no candidates" in detail_lower:
        return {
            "title": "Gemini returned no results",
            "message": "The Gemini API did not return any candidates.",
            "tip": "Your prompt may have been blocked by safety filters. Check your Gemini API settings.",
        }
    if "failed to parse" in detail_lower:
        return {
            "title": "AI response error",
            "message": "The AI model returned an unexpected format.",
            "tip": "This is likely a temporary issue. Try uploading the paper again.",
        }

    # ── Connection errors (wraps httpx.RequestError) ──
    if "connection" in detail_lower or "refused" in detail_lower:
        return {
            "title": "Cannot reach the server",
            "message": "The PaperLens backend is not running or unreachable.",
            "tip": "Make sure the API server is running (`uv run python run.py` or `uv run uvicorn app.main:app`).",
        }
    if "timeout" in detail_lower:
        return {
            "title": "Request timed out",
            "message": "The server took too long to respond.",
            "tip": "Your PDF may be very large, or the AI provider is slow. Try again or use a smaller file.",
        }

    # ── Fallback ──
    return {
        "title": "Something went wrong",
        "message": detail,
        "tip": None,
    }


def show_error(status_code: int, detail: str) -> None:
    err = friendly_error(status_code, detail)
    tip_html = ""
    if err["tip"]:
        tip_html = f'<div class="error-tip">💡 {err["tip"]}</div>'
    st.markdown(
        f'<div class="error-card">'
        f'  <div class="error-title">⚠️ {err["title"]}</div>'
        f'  <div class="error-body">{err["message"]}</div>'
        f'  {tip_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def _api_url(path: str) -> str:
    return f"{API_BASE.rstrip('/')}/{path.lstrip('/')}"


# ---------------------------------------------------------------------------
# Session state helpers
# ---------------------------------------------------------------------------

def _init_state() -> None:
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "page" not in st.session_state:
        st.session_state.page = "Upload & Analyse"


_init_state()


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown('<div class="sidebar-title">🔬 PaperLens</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sidebar-subtitle">Research Paper Analyser</div>',
        unsafe_allow_html=True,
    )

    selected = st.radio(
        "Navigation",
        options=["📤 Upload & Analyse", "📚 Previous Papers"],
        index=0 if st.session_state.page == "Upload & Analyse" else 1,
        label_visibility="collapsed",
        key="nav_radio",
    )
    # Map display label back to internal page name
    selected = selected.split(" ", 1)[1] if " " in selected else selected
    if selected != st.session_state.page:
        st.session_state.page = selected
        st.rerun()

    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    st.sidebar.markdown(
        '<div style="color:#475569;font-size:0.75rem;padding:0 1.5rem;">PaperLens v0.1.0</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Upload & Analyse page
# ---------------------------------------------------------------------------

def render_upload_page() -> None:
    st.markdown('<div class="page-title">📤 Upload a Research Paper</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-desc">Drop a PDF below and let AI analyse it for you.</div>',
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        help="Upload a research paper in PDF format (max 50 MB).",
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        st.markdown(
            f'<div class="card" style="padding:0.75rem 1rem;">'
            f'  <span style="font-weight:500;">📄 {uploaded_file.name}</span>'
            f'  <span style="color:#64748b;font-size:0.85rem;margin-left:0.75rem;">({file_size_mb:.1f} MB)</span>'
            f'</div>',
            unsafe_allow_html=True,
        )

        if file_size_mb > 50:
            st.error("File exceeds the 50 MB size limit.")
            st.stop()

        if st.button("🔬 Analyse Paper", type="primary", use_container_width=True):
            _run_analysis(uploaded_file)

    elif st.session_state.analysis:
        display_analysis(st.session_state.analysis)


def _run_analysis(uploaded_file) -> None:
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
                progress.progress(30, text="Uploading to server…")
                resp = client.post(_api_url("/upload"), files=files)

                if resp.is_error:
                    try:
                        detail = resp.json().get("detail", str(resp.reason_phrase))
                    except Exception:
                        detail = resp.reason_phrase or "Unknown server error"
                    status.update(label="Failed", state="error")
                    show_error(resp.status_code, detail)
                    return

                progress.progress(60, text="Analysing with AI…")
                data = resp.json()

                progress.progress(90, text="Finalising…")
                progress.progress(100, text="Done!")

        except httpx.HTTPStatusError as exc:
            try:
                detail = exc.response.json().get("detail", str(exc))
            except Exception:
                detail = str(exc)
            status.update(label="Failed", state="error")
            show_error(exc.response.status_code, detail)
            return

        except httpx.RequestError as exc:
            status.update(label="Failed", state="error")
            show_error(0, str(exc))
            return

        status.update(label="Analysis complete!", state="complete")

    st.balloons()
    st.session_state.analysis = data
    display_analysis(data)


# ---------------------------------------------------------------------------
# Display analysis results
# ---------------------------------------------------------------------------

def _metric_card(label: str, value: str) -> None:
    st.markdown(
        f'<div class="card" style="text-align:center;padding:1rem 0.5rem;">'
        f'  <div style="font-size:0.8rem;color:#64748b;text-transform:uppercase;letter-spacing:0.05em;">{label}</div>'
        f'  <div style="font-size:1.3rem;font-weight:700;color:#0f172a;margin-top:0.25rem;">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def display_analysis(data: dict) -> None:
    st.divider()

    title = data.get("title", "Untitled")
    st.markdown(
        f'<div class="page-title" style="margin-bottom:0.25rem;">📖 {title}</div>',
        unsafe_allow_html=True,
    )

    # Quick metrics
    s = data.get("summary", {})
    findings_count = len(s.get("key_findings", []))
    keywords_count = len(s.get("keywords", []))

    col1, col2, col3 = st.columns(3)
    with col1:
        _metric_card("Key Findings", str(findings_count))
    with col2:
        _metric_card("Keywords", str(keywords_count))
    with col3:
        abstract = data.get("abstract", "")
        has_abstract = "Yes" if abstract else "No"
        _metric_card("Abstract", has_abstract)

    st.markdown("<br>", unsafe_allow_html=True)

    # Abstract
    if abstract:
        with st.expander("📄 Abstract", expanded=False):
            st.write(abstract)

    # Executive Summary
    with st.expander("📋 Executive Summary", expanded=True):
        st.write(s.get("executive_summary", ""))

    # Key Findings
    with st.expander("🔑 Key Findings", expanded=findings_count <= 10):
        for finding in s.get("key_findings", []):
            st.markdown(f'<div style="padding:0.4rem 0;display:flex;gap:0.5rem;">'
                        f'  <span style="color:#2563eb;">●</span>'
                        f'  <span>{finding}</span>'
                        f'</div>', unsafe_allow_html=True)

    # Methodology
    with st.expander("🔬 Methodology", expanded=False):
        st.write(s.get("methodology", ""))

    # Conclusion
    with st.expander("🎯 Conclusion", expanded=False):
        st.write(s.get("conclusion", ""))

    # Keywords
    with st.expander("🏷️ Keywords", expanded=False):
        cols = st.columns(5)
        for i, kw in enumerate(s.get("keywords", [])):
            cols[i % 5].markdown(
                f'<span style="background:#e0e7ff;color:#3730a3;padding:0.2rem 0.6rem;'
                f'border-radius:12px;font-size:0.85rem;display:inline-block;margin:0.15rem 0;">'
                f'{kw}</span>',
                unsafe_allow_html=True,
            )

    # Simple Explanation
    with st.expander("💡 Simple Explanation", expanded=True):
        st.write(data.get("simple_explanation", ""))

    # Download
    report_path = data.get("report_path", "")
    if report_path:
        try:
            report_content = Path(report_path).read_text(encoding="utf-8")
            st.download_button(
                label="📥 Download Markdown Report",
                data=report_content,
                file_name=Path(report_path).name,
                mime="text/markdown",
                use_container_width=True,
            )
        except Exception:
            st.warning("Report file not available for download.")


# ---------------------------------------------------------------------------
# Previous papers page
# ---------------------------------------------------------------------------

def render_previous_papers() -> None:
    st.markdown('<div class="page-title">📚 Previously Analysed Papers</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-desc">Browse and revisit past analyses.</div>',
        unsafe_allow_html=True,
    )

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(_api_url("/papers"))
            resp.raise_for_status()
            papers = resp.json()
    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json().get("detail", str(exc))
        except Exception:
            detail = str(exc)
        show_error(exc.response.status_code, detail)
        return
    except httpx.RequestError as exc:
        show_error(0, str(exc))
        return

    if not papers:
        st.info(
            "No papers analysed yet. "
            "Go to **Upload & Analyse** to get started!",
            icon="📤",
        )
        return

    for p in papers:
        with st.container():
            st.markdown(
                f'<div class="card">'
                f'  <div style="display:flex;justify-content:space-between;align-items:center;">'
                f'    <div>'
                f'      <div style="font-weight:600;color:#0f172a;font-size:1rem;">📄 {p["title"]}</div>'
                f'      <div style="color:#64748b;font-size:0.85rem;margin-top:0.2rem;">'
                f'        {p["filename"]} · 🗓 {p["upload_date"][:10]}'
                f'      </div>'
                f'    </div>'
                f'  </div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if st.button("👁️ View Details", key=f"view_{p['id']}", use_container_width=True):
                with st.spinner("Fetching details…"):
                    try:
                        with httpx.Client(timeout=30) as client:
                            resp = client.get(_api_url(f"/papers/{p['id']}"))
                            resp.raise_for_status()
                            st.session_state.analysis = resp.json()
                    except httpx.HTTPStatusError as exc:
                        try:
                            detail = exc.response.json().get("detail", str(exc))
                        except Exception:
                            detail = str(exc)
                        show_error(exc.response.status_code, detail)
                        return
                    except httpx.RequestError as exc:
                        show_error(0, str(exc))
                        return
                st.session_state.page = "Upload & Analyse"
                st.rerun()


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

page = st.session_state.get("page", "Upload & Analyse")

if page == "Upload & Analyse":
    render_upload_page()
else:
    render_previous_papers()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.markdown('<div class="footer">🔬 PaperLens v0.1.0 — AI-powered research paper analysis</div>', unsafe_allow_html=True)
