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

# --- Done ---
echo ""
echo "🚀 PaperLens ready!"
echo ""
echo "  1. Edit .env with your API key(s)"
echo "  2. Run:  uv run python run.py"
echo "  3. Open  http://127.0.0.1:8501"
echo ""
