# 🔬 PaperLens

**Research paper analysis tool** — upload a PDF, get structured summaries, key findings, and a plain-English explanation.

PaperLens extracts text from a research paper via [PyMuPDF](https://pymupdf.readthedocs.io/), sends it to an LLM provider (OpenAI, Gemini, or local Ollama), and returns:

- **Executive Summary** – high-level overview (2–3 paragraphs)
- **Key Findings** – 5 major takeaways as bullet points
- **Methodology** – description of the methods used
- **Conclusion** – summary of conclusions
- **Keywords** – 5–10 important terms
- **Simple Explanation** – ≤300 words aimed at a motivated high-school student

Results can be downloaded as a Markdown report.

---

## Architecture

```
paperlens/
├── app/
│   ├── main.py                  FastAPI application (CORS, lifespan)
│   ├── config.py                Environment-based config via pydantic-settings
│   ├── database.py              SQLite CRUD for paper records
│   ├── exceptions.py            Custom error classes
│   ├── models/
│   │   └── paper.py             Pydantic models for all data shapes
│   ├── ai/
│   │   ├── base.py              Abstract AI provider interface
│   │   ├── factory.py           Provider factory (openai | gemini | ollama)
│   │   └── providers/
│   │       ├── openai.py        OpenAI (AsyncOpenAI SDK)
│   │       ├── gemini.py        Google Gemini (direct HTTP)
│   │       └── ollama.py        Local Ollama (direct HTTP)
│   ├── services/
│   │   ├── pdf_parser.py        Text extraction, title/abstract heuristics
│   │   ├── summarizer.py        Structured summary + simple explanation
│   │   ├── keyword_extractor.py Keyword extraction
│   │   └── report_generator.py  Markdown report generation
│   └── api/
│       └── routes.py            REST endpoints
├── frontend/
│   └── streamlit_app.py         Streamlit UI
├── tests/
│   ├── test_pdf_parser.py
│   ├── test_report_generator.py
│   └── test_database.py
├── pyproject.toml
├── .env.example
└── run.py                       Launch script
```

### Design decisions

- **AI provider abstraction** – the LLM provider implements a 3-method ABC (`generate`, `name`, `is_available`). The summarizer and keyword extractor never import an SDK directly. Adding a new provider means writing one class and registering it in the factory.
- **FastAPI backend + Streamlit frontend** – decoupled via HTTP. The frontend can be replaced with any web framework without touching the analysis pipeline.
- **Stateless services** – every service receives a provider instance; nothing is hard-wired to a specific model.

---

## Quick start

### Prerequisites

- Python ≥ 3.12
- [uv](https://docs.astral.sh/uv/) (package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/paperlens.git
cd paperlens

# Create a .env file from the template and add your API key(s)
cp .env.example .env

# Install dependencies
uv sync

# (Optional) Install dev dependencies for testing/linting
uv sync --extra dev
```

### Configuration

Edit `.env`:

```ini
# AI provider: openai, gemini, or ollama
AI_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Google Gemini
GEMINI_API_KEY=...
GEMINI_MODEL=gemini-2.0-flash

# Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
```

You only need to configure **one** provider. The rest can stay blank.

### Running

```bash
# Start both backend and frontend
uv run python run.py

# Start individually
uv run python run.py --api     # API only (http://127.0.0.1:8000)
uv run python run.py --ui      # UI only  (http://127.0.0.1:8501)
```

Open **http://127.0.0.1:8501** in your browser.

---

## API endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/upload` | Upload a PDF for analysis (multipart/form-data) |
| `GET`  | `/api/papers` | List all previously analysed papers |
| `GET`  | `/api/papers/{id}` | Full details for a single paper |
| `GET`  | `/api/reports/{path}` | Download a Markdown report file |

### Upload example

```bash
curl -X POST http://127.0.0.1:8000/api/upload \
  -F "file=@paper.pdf"
```

---

## Testing

```bash
uv sync --extra dev
uv run pytest tests/ -v
```

---

## Roadmap

- **Phase 2** – paper comparison, flashcard generation, citation extraction, PowerPoint export, research timelines
- **Phase 3** – batch processing, PDF annotation overlay, multi-user support

---

## License

MIT
