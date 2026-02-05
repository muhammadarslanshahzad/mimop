#!/bin/bash
# MiMoMop Setup Script
# Run this in WSL2 to set everything up

set -e  # Exit on error

echo "🤖 MiMoMop Setup Starting..."
echo ""

# Check if we're in WSL2
if ! grep -qi microsoft /proc/version; then
    echo "⚠️  Warning: This doesn't appear to be WSL2"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check for NVIDIA GPU
echo "🔍 Checking for NVIDIA GPU..."
if command -v nvidia-smi &> /dev/null; then
    echo "✅ NVIDIA GPU detected:"
    nvidia-smi --query-gpu=name --format=csv,noheader
else
    echo "⚠️  nvidia-smi not found. GPU passthrough may not be configured."
    echo "   You can continue, but LLM will be slower."
fi
echo ""

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
else
    echo "✅ uv already installed"
fi
echo ""

# Create virtual environment
echo "🐍 Setting up Python environment..."
if [ ! -d ".venv" ]; then
    uv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

# Activate venv
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
uv pip install numpy opencv-python qdrant-client requests websockets
echo "✅ Dependencies installed"
echo ""

# Check Ollama
echo "🦙 Checking Ollama installation..."
if ! command -v ollama &> /dev/null; then
    echo "📥 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    echo "✅ Ollama installed"
else
    echo "✅ Ollama already installed"
fi
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags &> /dev/null; then
    echo "🚀 Starting Ollama server..."
    ollama serve > /dev/null 2>&1 &
    OLLAMA_PID=$!
    echo "✅ Ollama started (PID: $OLLAMA_PID)"
    sleep 2
else
    echo "✅ Ollama already running"
fi
echo ""

# Pull required model
echo "📥 Downloading LLM model (gemma3:4b)..."
if ollama list | grep -q "gemma3:4b"; then
    echo "✅ Model already downloaded"
else
    ollama pull gemma3:4b
    echo "✅ Model downloaded"
fi
echo ""

# Test Ollama
echo "🧪 Testing Ollama..."
RESPONSE=$(ollama run gemma3:4b "Say 'MiMoMop ready!' in one sentence" --verbose=false 2>/dev/null || echo "failed")
if [[ $RESPONSE != "failed" ]]; then
    echo "✅ Ollama working!"
    echo "   Response: $RESPONSE"
else
    echo "⚠️  Ollama test failed, but continuing..."
fi
echo ""

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/{memory,maps,preferences}
echo "✅ Data directories created"
echo ""

echo "═══════════════════════════════════════════════════════════════"
echo "🎉 MiMoMop Setup Complete!"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Next steps:"
echo ""
echo "1. Copy this folder to Windows:"
echo "   cp -r ~/MiMoMop /mnt/c/Users/[YourName]/"
echo ""
echo "2. Open Webots (Windows) and load:"
echo "   C:\\Users\\[YourName]\\MiMoMop\\worlds\\mimomop_dev.wbt"
echo ""
echo "3. Click the ▶️  Play button in Webots"
echo ""
echo "4. Watch MiMoMop clean with attitude! 🧹✨"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Useful commands:"
echo "  source .venv/bin/activate     # Activate Python environment"
echo "  ollama serve &                # Start Ollama (if stopped)"
echo "  python3 -m pytest             # Run tests"
echo ""