#!/bin/bash
set -e

echo "🤖 Simple Agentic AI Demo - Quick Start"
echo "======================================="
echo ""

# Check Docker
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop."
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Start Ollama
echo "🚀 Starting Ollama..."
docker compose -f docker-compose-simple.yml up -d
echo "✓ Ollama started"
echo ""

# Check if model exists
if ! docker exec simple-ollama ollama list 2>/dev/null | grep -q "llama3.1"; then
    echo "📥 Pulling llama3.1 model (this will take a few minutes, ~4GB)..."
    docker exec simple-ollama ollama pull llama3.1
    echo "✓ Model pulled"
else
    echo "✓ Model already present"
fi
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -q -r simple-requirements.txt
echo "✓ Dependencies installed"
echo ""

echo "======================================="
echo "✅ Setup complete!"
echo ""
echo "Running the agent..."
echo "======================================="
echo ""

# Run the agent
python3 simple-agent.py

