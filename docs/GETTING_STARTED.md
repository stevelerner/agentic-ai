# Getting Started with Agentic AI Demo

This guide will help you set up and run the Agentic AI demonstration system.

## Prerequisites

Before you begin, ensure you have:

- **macOS** (tested on macOS 11+)
- **Docker Desktop** installed and running
  - Download from: https://www.docker.com/products/docker-desktop
  - At least 8GB RAM allocated to Docker
- **Terminal** access
- **Internet connection** (for pulling models and web search)

## Quick Start (Recommended)

The fastest way to get started:

```bash
cd /Volumes/external/code/agentic-ai
chmod +x quick-start.sh
./quick-start.sh
```

This script will:
1. Check Docker is running
2. Pull necessary images
3. Download the Ollama LLM model
4. Build application containers
5. Start all services
6. Open the web UI in your browser

**First-time setup takes 10-15 minutes** (mostly downloading the LLM model).

## Manual Setup

If you prefer manual control:

### Step 1: Start Ollama

```bash
docker compose up -d ollama
```

### Step 2: Pull the LLM Model

```bash
docker compose exec ollama ollama pull llama3.1
```

This downloads the llama3.1 model (~4GB). Wait for completion.

### Step 3: Build Containers

```bash
docker compose build
```

### Step 4: Start All Services

```bash
docker compose up -d
```

### Step 5: Verify Services

```bash
docker compose ps
```

You should see:
- `agentic-ollama` (running)
- `agentic-orchestrator` (running)
- `agentic-sandbox` (running)
- `agentic-ui` (running)

## Using the System

### Web UI (Recommended for Beginners)

1. Open http://localhost:8080 in your browser
2. You'll see the main interface with:
   - Agent status panel (left)
   - Chat interface (center)
   - Execution details (right)
3. Try an example prompt or type your own
4. Watch agents collaborate in real-time

**Example prompts:**
- "Research AI agent frameworks and create a comparison report"
- "Generate a Python REST API with authentication"
- "Explain quantum computing and write a beginner's guide"

### CLI Mode

For command-line interaction:

```bash
make cli
```

Or manually:

```bash
docker compose exec orchestrator python cli.py
```

Type your tasks and press Enter. Type `quit` to exit.

### API Access

The REST API is available at http://localhost:8000

Interactive docs: http://localhost:8000/docs

**Example API call:**

```bash
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"query": "Research latest AI trends"}'
```

## Running Examples

Pre-built example scenarios:

```bash
# Run all examples
make examples

# Or individually:
make example-research   # Research task
make example-analysis   # Data analysis
make example-coding     # Code generation
```

## Monitoring

### View Logs

```bash
# All services
make logs

# Specific service
docker compose logs -f orchestrator
docker compose logs -f ollama
```

### Check Service Status

```bash
make status
# or
docker compose ps
```

### Health Check

```bash
curl http://localhost:8000/health
```

## Common Tasks

### Stop Services

```bash
make stop
# or
docker compose stop
```

### Restart Services

```bash
make restart
# or
docker compose restart
```

### Clean Up

```bash
# Stop and remove containers
make clean

# Complete cleanup (including volumes and outputs)
make clean-all
```

### Reset Agents

If agents get stuck or behave unexpectedly:

```bash
curl -X POST http://localhost:8000/api/orchestrator/reset
```

## Troubleshooting

### Issue: "Docker is not running"

**Solution:** Start Docker Desktop and wait for it to be fully running.

### Issue: Ollama model pull fails

**Solution:**
1. Check internet connection
2. Ensure enough disk space (~10GB free)
3. Try pulling manually:
   ```bash
   docker compose exec ollama ollama pull llama3.1
   ```

### Issue: Services won't start

**Solution:**
1. Check Docker resource allocation (need 8GB+ RAM)
2. View logs: `docker compose logs`
3. Try clean restart:
   ```bash
   make clean
   make setup
   ```

### Issue: Web UI shows "Disconnected"

**Solution:**
1. Check orchestrator is running: `docker compose ps orchestrator`
2. Check API health: `curl http://localhost:8000/health`
3. View orchestrator logs: `docker compose logs orchestrator`

### Issue: Agents respond slowly

**Cause:** LLM inference is CPU/GPU intensive.

**Solutions:**
- Allocate more resources to Docker
- Be patient - responses take 10-60 seconds depending on complexity
- Consider using a smaller model (llama3.1:8b instead of default)

### Issue: Web search fails

**Solution:**
1. Check internet connection
2. DuckDuckGo may rate-limit - wait a minute and try again
3. Check orchestrator logs for specific errors

### Issue: Port already in use

**Solution:**
1. Check what's using the port:
   ```bash
   lsof -i :8080  # or :8000, :11434
   ```
2. Stop the conflicting service or change ports in `docker-compose.yml`

## Configuration

### Environment Variables

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - OLLAMA_MODEL=llama3.1        # Change model
  - LLM_TEMPERATURE=0.2          # Creativity (0-1)
  - LLM_MAX_TOKENS=2000          # Response length
  - MAX_ITERATIONS=10            # Max reasoning loops
  - ENABLE_MEMORY=true           # Long-term memory
  - MAX_SEARCH_RESULTS=10        # Web search results
```

### Using a Different Model

1. Pull a different model:
   ```bash
   docker compose exec ollama ollama pull mistral
   ```

2. Update `docker-compose.yml`:
   ```yaml
   - OLLAMA_MODEL=mistral
   ```

3. Restart orchestrator:
   ```bash
   docker compose restart orchestrator
   ```

### Accessing Outputs

Generated files are saved in `./outputs/`:

```bash
ls -la outputs/
cat outputs/report.md
```

## Next Steps

- **Explore Examples:** Run the example scenarios to see different use cases
- **Read Architecture:** Check `docs/ARCHITECTURE.md` for system design
- **Customize Agents:** Modify agent prompts and tools in `agents/`
- **Add Tools:** Create new tools in `tools/` for agents to use
- **Experiment:** Try complex multi-step tasks to see agent collaboration

## Getting Help

- **Check Logs:** Most issues are visible in logs
  ```bash
  make logs
  ```

- **Health Check:** Verify all services are healthy
  ```bash
  curl http://localhost:8000/health
  ```

- **Clean Restart:** When in doubt, clean and restart
  ```bash
  make clean-all
  make setup
  ```

## Performance Tips

1. **First Request is Slow:** Ollama loads model on first use (~10-30 seconds)
2. **Subsequent Requests:** Much faster after model is loaded
3. **Concurrent Requests:** System handles one task at a time by design
4. **Resource Usage:** Monitor Docker Desktop resource usage
5. **Disk Space:** Ensure 15GB+ free space for models and outputs

## Security Notes

- System runs locally - no data sent to external services except web search
- Code execution is sandboxed but runs locally
- Don't process sensitive data without additional security measures
- Web UI has no authentication - meant for local development only

---

Enjoy exploring agentic AI principles! 🤖

