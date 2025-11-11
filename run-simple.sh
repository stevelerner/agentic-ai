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

# Create outputs directory
mkdir -p outputs

# Start services
echo "🚀 Starting services..."
docker compose -f docker-compose-simple.yml up -d --build
echo "✓ Services started"
echo ""

# Wait for Ollama
echo "⏳ Waiting for Ollama to be ready..."
sleep 5

# Check if model exists
if ! docker exec simple-ollama ollama list 2>/dev/null | grep -q "llama3.1"; then
    echo "📥 Pulling llama3.1 model (this will take a few minutes, ~4GB)..."
    docker exec simple-ollama ollama pull llama3.1
    echo "✓ Model pulled"
else
    echo "✓ Model already present"
fi
echo ""

echo "======================================="
echo "✅ Setup complete!"
echo ""
echo "🌐 Web UI: http://localhost:8000"
echo ""
echo "Containers running in background."
echo ""
echo "Useful commands:"
echo "  docker compose -f docker-compose-simple.yml logs -f web    # View logs"
echo "  docker compose -f docker-compose-simple.yml ps             # Check status"
echo "  docker compose -f docker-compose-simple.yml down           # Stop"
echo "======================================="
echo ""

# Open browser automatically (optional)
if command -v open &> /dev/null; then
    sleep 2
    open http://localhost:8000
fi

