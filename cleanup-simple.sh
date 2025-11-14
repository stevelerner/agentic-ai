#!/bin/bash
set -e

echo "🧹 Cleaning up Simple Agentic AI Demo"
echo "======================================="
echo ""

# Check Docker before attempting cleanup
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker is not running. Skipping cleanup."
    echo ""
    echo "Note: Containers may still be running if Docker was stopped while they were active."
    echo "When Docker is running again, you can manually clean up with:"
    echo "  docker compose -f docker-compose-simple.yml down"
    echo ""
    return 2>/dev/null || exit 0
fi

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

