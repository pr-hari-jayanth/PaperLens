#!/usr/bin/env bash
set -euo pipefail

echo "🔬 PaperLens setup"
echo "=================="
echo ""

# --- .env ---
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📄 Created .env from .env.example — edit it with your API keys."
else
    echo "✅ .env already exists."
fi

# --- Python & uv ---
if ! command -v uv &>/dev/null; then
    echo "❌ 'uv' not found. Install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "📦 Installing Python dependencies..."
uv sync --quiet
echo "✅ Dependencies installed."

# --- Landing page ---
echo ""
echo "🎨 Building landing page..."
if command -v npm &>/dev/null; then
    (cd frontend/landing && npm install --silent && npm run build --silent)
    echo "✅ Landing page built."
else
    echo "⚠️  npm not found — skipping landing page build."
    echo "   The API will still serve the landing page at http://127.0.0.1:8000"
    echo "   if you build it later with: cd frontend/landing && npm install && npm run build"
fi

# --- Done ---
echo ""
echo "🚀 PaperLens ready!"
echo ""
echo "  1. Edit .env with your API key(s)"
echo "  2. Run:  uv run python run.py"
echo "  3. Open  http://127.0.0.1:8000  (upload & analyse papers)"
echo "  4. Run with --legacy-ui to also start the legacy Streamlit app on port 8501"
echo ""
