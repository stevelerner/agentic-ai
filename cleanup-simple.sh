#!/bin/bash
set -e

echo "🧹 Cleaning up Simple Agentic AI Demo"
echo "======================================="
echo ""

# Stop and remove containers
echo "Stopping containers..."
docker compose -f docker-compose-simple.yml down

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Kept:"
echo "  ✓ Ollama image (no re-download needed)"
echo "  ✓ llama3.1 model (no re-download needed)"
echo "  ✓ Volume data preserved"
echo ""
echo "Removed:"
echo "  ✓ Running containers"
echo "  ✓ Container networks"
echo ""
echo "To start again: ./run-simple.sh"
echo ""

