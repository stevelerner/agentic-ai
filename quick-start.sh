#!/bin/bash
set -e

echo "🤖 Agentic AI Demo - Quick Start"
echo "================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker Desktop and try again"
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
    echo "❌ Error: docker-compose not found"
    echo "Please install docker-compose and try again"
    exit 1
fi

# Use 'docker compose' or 'docker-compose' depending on what's available
if docker compose version &> /dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

echo "✓ docker-compose is available"
echo ""

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p outputs
mkdir -p sandbox_workspace
echo "✓ Directories created"
echo ""

# Pull Ollama image
echo "📥 Pulling Ollama image (this may take a few minutes)..."
docker pull ollama/ollama:latest
echo "✓ Ollama image pulled"
echo ""

# Start Ollama service
echo "🚀 Starting Ollama service..."
$DOCKER_COMPOSE up -d ollama
echo "✓ Ollama service started"
echo ""

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to be ready..."
sleep 10
echo "✓ Ollama is ready"
echo ""

# Pull the LLM model
echo "📥 Pulling llama3.1 model (this may take several minutes)..."
$DOCKER_COMPOSE exec ollama ollama pull llama3.1
echo "✓ Model pulled"
echo ""

# Build application containers
echo "🔨 Building application containers..."
$DOCKER_COMPOSE build
echo "✓ Containers built"
echo ""

# Start all services
echo "🚀 Starting all services..."
$DOCKER_COMPOSE up -d
echo "✓ All services started"
echo ""

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Check health
MAX_ATTEMPTS=30
ATTEMPT=0
while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✓ Services are healthy"
        break
    fi
    ATTEMPT=$((ATTEMPT + 1))
    sleep 2
done

if [ $ATTEMPT -eq $MAX_ATTEMPTS ]; then
    echo "⚠️  Warning: Services may not be fully ready yet"
    echo "Check status with: docker-compose logs"
fi

echo ""
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "🌐 Web UI:  http://localhost:8080"
echo "📡 API:     http://localhost:8000/docs"
echo ""
echo "Try these commands:"
echo "  make cli              - Interactive CLI mode"
echo "  make logs             - View all logs"
echo "  make examples         - Run example scenarios"
echo "  make stop             - Stop all services"
echo ""
echo "Opening web UI in your browser..."
sleep 2

# Try to open browser
if command -v open &> /dev/null; then
    open http://localhost:8080
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8080
else
    echo "Please open http://localhost:8080 in your browser"
fi

