# Agentic AI Demo - Multi-Agent Orchestration System

A comprehensive demonstration of modern agentic AI principles with detailed implementation of core computer science and AI concepts. This project shows not just WHAT agentic AI does, but HOW it works at the code level.

## Core AI & Computer Science Principles

This demo implements and demonstrates 14 fundamental concepts from modern AI, distributed systems, and software architecture:

**AI/ML Concepts:**
- Agent Architecture & Reasoning Loops
- Multi-Agent Systems & Orchestration  
- Tool Use & Function Calling
- Planning & Task Decomposition
- Memory Systems & Context Management
- **RAG (Retrieval-Augmented Generation)**
- **Chain-of-Thought (CoT) & ReAct Pattern**
- **Embeddings & Vector Similarity**
- Prompt Engineering

**Computer Science Concepts:**
- Asynchronous Task Processing
- Sandboxed Code Execution
- REST API & Service Architecture
- Real-Time Communication (WebSockets)
- Containerization & Orchestration

Each principle below includes: concept definition, implementation location, code examples, and underlying CS theory.

### 1. Agent Architecture & Reasoning Loops

**Concept**: Autonomous agents that perceive, reason, and act iteratively until reaching a goal.

**Implementation**: `agents/base_agent.py`
- **Perception**: Agents receive input and parse it with context
- **Reasoning**: LLM generates next action based on system prompt + history
- **Action**: Execute tool calls or return final response
- **Iteration**: Loop continues until task completion or max iterations

```python
# Key method: BaseAgent.think() implements the reasoning loop
def think(self, user_message: str, context: Dict = None) -> str:
    for iteration in range(max_iterations):
        response = self.call_llm(messages)
        tool_call = self.parse_tool_call(response)
        if tool_call:
            result = self.execute_tool(tool_name, arguments)
            # Continue loop with tool result
        else:
            return response  # Task complete
```

**CS Principle**: Finite state machine with feedback loops

### 2. Multi-Agent Systems & Orchestration

**Concept**: Multiple specialized agents coordinate to solve complex problems that single agents cannot handle efficiently.

**Implementation**: `agents/orchestrator.py`
- **Decomposition**: Planner agent breaks tasks into sub-tasks
- **Delegation**: Orchestrator routes sub-tasks to specialist agents
- **Dependency Management**: Tracks which steps depend on others
- **Synthesis**: Combines results from multiple agents

```python
# Key method: Orchestrator.process_task()
# 1. Plan creation (task decomposition)
plan = self.planner.create_plan(user_query)

# 2. Execute steps with dependency resolution
for step in plan.steps:
    if dependencies_satisfied(step):
        agent = self.agents[step.agent]
        result = agent.think(step.action, context)
        
# 3. Synthesize final result
return self._synthesize_results(plan, results)
```

**CS Principles**: Directed acyclic graph (DAG) execution, distributed systems coordination

### 3. Tool Use & Function Calling

**Concept**: LLMs augmented with external tools/APIs to perform actions beyond text generation.

**Implementation**: `agents/base_agent.py` + `tools/`
- **Tool Schema Definition**: Each tool has name, description, parameters
- **Structured Output Parsing**: Extract JSON function calls from LLM responses
- **Safe Execution**: Validate and execute tools in controlled environment
- **Result Integration**: Feed tool output back to LLM for reasoning

```python
# Tool definition pattern (see tools/*.py)
TOOLS = {
    "web_search": {
        "description": "Search the web",
        "function": web_search,
        "parameters": {"query": "string", "max_results": "int"}
    }
}

# LLM generates structured call:
{"tool": "web_search", "arguments": {"query": "AI trends", "max_results": 5}}

# Agent executes and continues reasoning with result
```

**CS Principles**: Remote procedure call (RPC), API design, input validation

### 4. Planning & Hierarchical Task Decomposition

**Concept**: Breaking complex tasks into manageable sub-tasks with dependencies.

**Implementation**: `agents/planner.py`
- **Task Analysis**: LLM analyzes requirements and constraints
- **Hierarchical Decomposition**: Creates step-by-step execution plan
- **Dependency Graph**: Identifies which steps must complete before others
- **Agent Selection**: Assigns appropriate specialist to each step

```python
# Planner output structure (JSON):
{
    "steps": [
        {"id": 1, "agent": "researcher", "action": "...", "dependencies": []},
        {"id": 2, "agent": "analyst", "action": "...", "dependencies": [1]},
        {"id": 3, "agent": "writer", "action": "...", "dependencies": [1, 2]}
    ]
}
```

**CS Principles**: Topological sorting, dependency resolution, task scheduling

### 5. Memory Systems & Context Management

**Concept**: Agents maintain context across interactions to enable coherent conversations and learning.

**Implementation**: `memory/short_term.py` + `memory/long_term.py`

**Short-term Memory** (Conversation Context):
- **Sliding Window**: Keep last N messages to stay within token limits
- **Fast Retrieval**: O(1) access to recent context
- **Implementation**: Python deque (double-ended queue)

**Long-term Memory** (Persistent Knowledge):
- **Storage**: JSON-based persistence (production would use vector DB)
- **Retrieval**: Keyword-based search (production would use embeddings)
- **Use Case**: Learn from past tasks, avoid redundant work

```python
# Short-term: memory/short_term.py
class ShortTermMemory:
    def __init__(self, max_messages=20):
        self.messages = deque(maxlen=max_messages)  # Auto-eviction

# Long-term: memory/long_term.py
class LongTermMemory:
    def store(self, content, metadata):
        # Persist to disk
    def retrieve(self, query, top_k=5):
        # Similarity search (simplified)
```

**CS Principles**: Caching, LRU eviction, information retrieval, vector similarity

### 6. RAG (Retrieval-Augmented Generation)

**Concept**: Enhance LLM responses by retrieving relevant information from external knowledge sources before generation.

**Implementation**: `memory/long_term.py` + agent tool use

The system demonstrates RAG principles in two ways:

**1. Tool-Based RAG** (Web Search):
```python
# agents/researcher.py + tools/web_search.py
# Agent realizes it needs information
response = '{"tool": "web_search", "arguments": {"query": "AI trends 2024"}}'

# Retrieve relevant documents
search_results = web_search("AI trends 2024", max_results=5)

# Augment next LLM call with retrieved information
context = f"Search results: {search_results}"
final_response = llm(user_query + context)  # Generate with retrieval
```

**2. Memory-Based RAG** (Long-term Memory):
```python
# memory/long_term.py
class LongTermMemory:
    def retrieve(self, query: str, top_k: int = 5):
        """Retrieve relevant past experiences"""
        # Current: keyword-based similarity
        # Production: would use embeddings + vector DB
        scored_memories = []
        for memory in self.memories:
            score = similarity(query, memory.content)  # Semantic similarity
            scored_memories.append((score, memory))
        return top_k_results(scored_memories)

# Usage in agent
relevant_past_tasks = long_term_memory.retrieve(current_query)
response = llm(query + relevant_past_tasks)  # Augmented generation
```

**RAG Pipeline**:
1. **Query**: User asks a question
2. **Retrieval**: Fetch relevant documents (web search or memory)
3. **Augmentation**: Combine query + retrieved context
4. **Generation**: LLM generates response with retrieved context

**CS Principles**: Information retrieval, semantic search, context injection

**Production Enhancement**: Replace keyword matching with:
```python
# Vector embeddings for semantic search
from sentence_transformers import SentenceTransformer
import chromadb

# Embed and store
embeddings = model.encode(documents)
vector_db.add(embeddings, documents)

# Retrieve by semantic similarity
query_embedding = model.encode(query)
relevant_docs = vector_db.search(query_embedding, top_k=5)
```

### 7. Chain-of-Thought (CoT) & ReAct Pattern

**Concept**: Make LLM reasoning explicit through step-by-step thought processes, combined with tool use.

**Implementation**: Agent reasoning loops demonstrate **ReAct** (Reasoning + Acting)

```python
# agents/base_agent.py - implements ReAct pattern
def think(self, user_message: str) -> str:
    for iteration in range(max_iterations):
        # REASONING: LLM thinks about what to do
        response = self.call_llm(messages)
        # "To answer this, I need to search for recent data..."
        
        # ACTION: Execute tool based on reasoning
        if tool_call := self.parse_tool_call(response):
            # "Calling web_search with query='AI trends 2024'"
            result = self.execute_tool(tool_name, arguments)
            
            # OBSERVATION: Add result to context for next reasoning step
            messages.append({
                "role": "user",
                "content": f"Tool result: {result}"
            })
            # Loop continues: Reason → Act → Observe → Reason → ...
        else:
            return response  # Final answer after reasoning chain
```

**ReAct Trace Example**:
```
Thought 1: "I need current information about AI agents"
Action 1: web_search("AI agents 2024")
Observation 1: [search results...]

Thought 2: "Now I should analyze the key trends from these sources"
Action 2: analyze_data(search_results)
Observation 2: [analysis results...]

Thought 3: "I have enough information to write a summary"
Action 3: No action needed
Final Answer: [comprehensive summary]
```

**Chain-of-Thought Benefits**:
- Makes reasoning transparent and debuggable
- Breaks complex problems into steps
- Allows error recovery (if action fails, reason about alternative)

**CS Principles**: State machines, iterative refinement, trace logging

### 8. Embeddings & Vector Similarity

**Concept**: Represent text as dense vectors in high-dimensional space where semantic similarity = geometric proximity.

**Current Implementation**: Simplified keyword matching in `memory/long_term.py`

**Production Pattern** (how it should work):
```python
# memory/long_term.py (production version)
from sentence_transformers import SentenceTransformer
import numpy as np

class LongTermMemory:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = []  # Vector representations
        self.memories = []    # Original text
    
    def store(self, content: str, metadata: dict):
        # Convert text to 384-dim vector
        embedding = self.encoder.encode(content)
        self.embeddings.append(embedding)
        self.memories.append(content)
    
    def retrieve(self, query: str, top_k: int = 5):
        # Encode query to same vector space
        query_embedding = self.encoder.encode(query)
        
        # Compute cosine similarity with all stored vectors
        similarities = []
        for i, mem_embedding in enumerate(self.embeddings):
            # Cosine similarity = dot product / (norm1 * norm2)
            sim = np.dot(query_embedding, mem_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(mem_embedding)
            )
            similarities.append((sim, self.memories[i]))
        
        # Return top-k most similar
        return sorted(similarities, reverse=True)[:top_k]
```

**Why Embeddings?**
- **Semantic Understanding**: "car" and "automobile" have similar vectors
- **Multilingual**: Cross-language similarity
- **Efficient**: Vector operations are fast (SIMD, GPU-accelerated)
- **Approximate**: No need for exact keyword matches

**Vector Databases** (ChromaDB, Pinecone, Weaviate):
```python
# Using ChromaDB (referenced in requirements.txt)
import chromadb

client = chromadb.Client()
collection = client.create_collection("agent_memory")

# Add documents with automatic embedding
collection.add(
    documents=["Agent completed research task...", "Analysis of data..."],
    ids=["task_1", "task_2"]
)

# Query returns semantically similar documents
results = collection.query(
    query_texts=["find information about research"],
    n_results=5
)
```

**CS Principles**: Linear algebra, cosine similarity, nearest neighbor search, high-dimensional geometry

### 9. Prompt Engineering & System Prompts

**Concept**: Carefully crafted instructions that define agent behavior and capabilities.

**Implementation**: Each agent class defines `get_system_prompt()`

Example from `agents/researcher.py`:
```python
def get_system_prompt(self) -> str:
    return """You are a research agent specialized in gathering information.

Your capabilities:
- Search the web for current information
- Evaluate source credibility
- Synthesize findings from multiple sources
- Cite sources properly

When you need to search, respond with:
{"tool": "web_search", "arguments": {"query": "...", "max_results": 5}}

After gathering information, provide:
1. Key findings (bullet points)
2. Source citations (with URLs)
...
"""
```

**Prompt Engineering Techniques Used**:
- **Role Definition**: "You are a research agent specialized in..."
- **Capability Listing**: Explicit list of what agent can do
- **Output Format**: Structured JSON for tool calls
- **Task Decomposition**: Step-by-step instructions
- **Examples**: Show desired output format

**Few-Shot Prompting** (not currently implemented, but easily added):
```python
system_prompt = """You are a research agent.

Example interaction:
User: "Find papers on quantum computing"
Assistant: {"tool": "web_search", "arguments": {"query": "quantum computing papers 2024"}}
Tool result: [list of papers]
Assistant: "Here are key papers on quantum computing..."

Now handle this request:"""
```

**CS Principles**: Domain-specific languages (DSL), behavior specification, constraint programming

### 10. Asynchronous Task Processing

**Concept**: Handle long-running tasks without blocking, provide real-time updates.

**Implementation**: `api/main.py`
- **Task Queue**: FastAPI async endpoints
- **Background Processing**: asyncio for concurrent execution
- **WebSocket Updates**: Real-time status notifications
- **State Management**: Track task status (pending/processing/completed)

```python
# api/main.py
@app.post("/api/task")
async def create_task(request: TaskRequest):
    task_id = generate_id()
    tasks[task_id] = {"status": "pending", ...}
    
    # Process asynchronously
    asyncio.create_task(process_task(task_id))
    
    return {"task_id": task_id, "status": "pending"}

# WebSocket broadcasts updates
await broadcast_task_update(task_id, "completed")
```

**CS Principles**: Asynchronous I/O, event-driven architecture, pub-sub pattern

### 11. Sandboxed Code Execution

**Concept**: Safely execute untrusted code in isolated environment.

**Implementation**: `tools/code_runner.py` + Docker
- **Process Isolation**: Run code in subprocess with timeout
- **Container Isolation**: Separate Docker container (Dockerfile.sandbox)
- **Resource Limits**: CPU, memory, and time constraints
- **Network Restriction**: No external network access

```python
# tools/code_runner.py
def execute_code(code: str, timeout: int = 30):
    result = subprocess.run(
        ["python3", temp_file],
        capture_output=True,
        timeout=timeout  # Kill if exceeds
    )
    return {"output": result.stdout, "exitcode": result.returncode}
```

**CS Principles**: Process isolation, containerization, security sandboxing

### 12. REST API & Service Architecture

**Concept**: Expose functionality via standard HTTP interface with proper separation of concerns.

**Implementation**: `api/main.py` (FastAPI)
- **Resource-based Endpoints**: `/api/task`, `/api/agents`, `/api/memory`
- **Async Request Handling**: Non-blocking I/O for concurrent requests
- **Auto-generated Documentation**: OpenAPI/Swagger from type hints
- **CORS Support**: Enable cross-origin requests for web UI

```python
# api/main.py
@app.post("/api/task", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    # Type validation via Pydantic
    # Async processing
    # Structured response
```

**CS Principles**: RESTful design, service-oriented architecture, API contracts

### 13. Real-Time Communication & WebSockets

**Concept**: Bidirectional communication for live updates without polling.

**Implementation**: `api/main.py` WebSocket endpoint + `ui/app.js`
- **Connection Management**: Track active WebSocket connections
- **Event Broadcasting**: Notify all clients of task updates
- **Reconnection Logic**: Client automatically reconnects on disconnect

```python
# Server: api/main.py
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    # Broadcast updates to all connected clients

# Client: ui/app.js
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'task_update') {
        updateUI(data);
    }
}
```

**CS Principles**: WebSocket protocol, event-driven UI, real-time systems

### 14. Containerization & Service Orchestration

**Concept**: Package applications with dependencies for consistent deployment across environments.

**Implementation**: `docker-compose.yml` + Dockerfiles
- **Service Isolation**: Each component in separate container
- **Dependency Management**: Docker Compose defines service relationships
- **Volume Mounting**: Share data between containers and host
- **Health Checks**: Monitor service availability

```yaml
# docker-compose.yml
services:
  ollama:           # LLM server
  orchestrator:     # Agent system
  sandbox:          # Code execution
  ui:               # Web interface
  
# Inter-service communication via Docker network
```

**CS Principles**: Containerization, service mesh, infrastructure as code

## Technical Stack & Design Decisions

### Why Ollama (Local LLM)?
- **Privacy**: No data sent to external APIs
- **Cost**: No per-token charges
- **Latency**: Predictable local inference
- **Learning**: Understand LLM integration without API abstractions

### Why FastAPI?
- **Async Support**: Native async/await for concurrent requests
- **Type Safety**: Pydantic models for validation
- **Auto Documentation**: OpenAPI spec generation
- **Modern Python**: Leverages type hints and async features

### Why Multi-Agent Architecture?
- **Separation of Concerns**: Each agent has clear responsibility
- **Specialized Prompts**: Optimized instructions per domain
- **Parallel Execution**: Independent agents can work concurrently (future)
- **Modularity**: Easy to add/remove/modify agents

### Why Docker Compose?
- **Reproducibility**: Works identically on any system
- **Isolation**: Services don't interfere with each other
- **Simplicity**: Single command to start entire system
- **Production Parity**: Similar to real deployment environments

## Quick Start

### Prerequisites

- macOS with Docker Desktop installed
- 8GB+ RAM available for containers
- Internet connection

### Option 1: Quick Start (Recommended)

```bash
cd /Volumes/external/code/agentic-ai
make setup    # Pull Ollama model and build containers
make run      # Start the system
```

Then open: http://localhost:8080

### Option 2: Manual Setup

```bash
# 1. Start Ollama and pull model
docker compose up -d ollama
docker compose exec ollama ollama pull llama3.1

# 2. Build and start all services
docker compose up --build

# 3. Open the UI
open http://localhost:8080
```

## Project Structure

```
agentic-ai/
├── docker-compose.yml          # Multi-container orchestration
├── Makefile                    # Convenience commands
├── agents/                     # Agent implementations
│   ├── base_agent.py          # Base agent class
│   ├── planner.py             # Planning agent
│   ├── researcher.py          # Research agent
│   ├── analyst.py             # Analysis agent
│   ├── writer.py              # Writing agent
│   ├── coder.py               # Coding agent
│   └── orchestrator.py        # Multi-agent coordinator
├── tools/                     # Agent tools
│   ├── web_search.py          # DuckDuckGo search
│   ├── file_ops.py            # File operations
│   ├── code_runner.py         # Safe code execution
│   └── data_tools.py          # Data analysis tools
├── memory/                    # Memory systems
│   ├── short_term.py          # Conversation memory
│   └── long_term.py           # Vector-based retrieval
├── api/                       # FastAPI backend
│   ├── main.py                # API server
│   └── models.py              # Pydantic models
├── ui/                        # Web interface
│   ├── index.html             # Main UI
│   ├── app.js                 # Frontend logic
│   └── styles.css             # Styling
└── examples/                  # Demo scenarios
    ├── research_task.py       # Research example
    ├── analysis_task.py       # Analysis example
    └── coding_task.py         # Code generation example
```

## Example Use Cases

### 1. Research & Report Generation

```
Ask: "Research the latest trends in AI agents and write a comprehensive 
report with sources, analysis, and future predictions"

Flow:
Planner → Creates multi-step plan
Researcher → Searches web for recent articles
Analyst → Synthesizes findings and identifies trends
Writer → Generates structured report with citations
```

### 2. Data Analysis Pipeline

```
Ask: "Analyze this CSV file, identify trends, create visualizations, 
and provide recommendations"

Flow:
Planner → Breaks down analysis steps
Analyst → Loads data, performs statistical analysis
Coder → Generates visualization code
Analyst → Interprets results and creates recommendations
Writer → Formats final report
```

### 3. Code Generation with Research

```
Ask: "Research best practices for REST APIs in Python and generate 
a production-ready implementation with tests"

Flow:
Researcher → Finds current best practices
Planner → Designs API architecture
Coder → Generates implementation code
Coder → Writes comprehensive tests
Writer → Creates documentation
```

## Architecture

### Agent Communication Pattern

```
User Query
    ↓
Orchestrator (receives task)
    ↓
Planner (creates execution plan)
    ↓
Orchestrator (delegates sub-tasks)
    ├→ Researcher (gathers information)
    ├→ Analyst (processes data)
    ├→ Coder (generates code)
    └→ Writer (creates output)
    ↓
Orchestrator (synthesizes results)
    ↓
Reflection Loop (if needed)
    ↓
Final Output
```

### Technology Stack

- **LLM**: Ollama (llama3.1) - runs in container
- **Backend**: Python 3.12 + FastAPI
- **Frontend**: Vanilla JS + WebSockets (real-time updates)
- **Search**: DuckDuckGo API
- **Memory**: In-memory + ChromaDB for embeddings
- **Containers**: Docker Compose

## Using the System

### Via Web UI (Recommended)

1. Navigate to http://localhost:8080
2. Enter your task in the chat interface
3. Watch agents collaborate in real-time
4. View reasoning traces and tool calls
5. Download generated artifacts

### Via API

```bash
# Submit a task
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"query": "Research AI safety and write a summary"}'

# Check task status
curl http://localhost:8000/api/task/{task_id}

# Get results
curl http://localhost:8000/api/task/{task_id}/result
```

### Via CLI

```bash
# Interactive mode
make cli

# Single command
docker compose exec orchestrator python -m cli \
  "Research quantum computing trends"
```

## Monitoring & Debugging

```bash
# View all logs
make logs

# View specific service
docker compose logs -f orchestrator

# View agent reasoning traces
curl http://localhost:8000/api/traces

# Check memory state
curl http://localhost:8000/api/memory/stats
```

## Configuration

Edit `docker-compose.yml` or set environment variables:

```bash
# LLM Configuration
OLLAMA_MODEL=llama3.1              # Model to use
LLM_TEMPERATURE=0.2                # Creativity (0-1)
LLM_MAX_TOKENS=2000                # Response length

# Agent Configuration
MAX_ITERATIONS=10                  # Max reflection loops
ENABLE_MEMORY=true                 # Use long-term memory
VERBOSE_LOGGING=false              # Debug output

# Tool Configuration
MAX_SEARCH_RESULTS=10              # Web search limit
ENABLE_CODE_EXECUTION=true         # Allow code runner
SANDBOX_TIMEOUT=30                 # Code timeout (seconds)
```

## Running Examples

```bash
# Research task
make example-research

# Data analysis task
make example-analysis

# Code generation task
make example-coding

# Run all examples
make examples
```

## Stopping the System

```bash
# Stop all containers
make stop

# Stop and remove volumes
make clean

# Complete cleanup
make clean-all
```

## Security Notes

- Code execution runs in sandboxed containers
- Network access is restricted for code runner
- No file system access outside mounted volumes
- LLM runs locally (no data sent to external APIs)

## Code Walkthrough for Learning

### Understanding the Codebase

This project is structured for educational exploration. Here's how to read and understand the code:

#### Start Here: Core Agent Logic
1. **`agents/base_agent.py`** (200 lines)
   - Read `think()` method first - this is the reasoning loop
   - Understand `parse_tool_call()` - how agents detect function calls
   - Study `execute_tool()` - tool execution pattern
   - **Key Concept**: Perception-Reasoning-Action cycle

2. **`agents/orchestrator.py`** (150 lines)
   - Read `process_task()` - multi-agent coordination
   - Understand `_synthesize_results()` - result aggregation
   - **Key Concept**: Task delegation and dependency management

3. **`agents/planner.py`** (100 lines)
   - Read `create_plan()` - task decomposition logic
   - Notice the JSON structure for plans
   - **Key Concept**: Hierarchical planning with dependencies

#### Tool Implementation
4. **`tools/web_search.py`** (50 lines)
   - Simple tool pattern: input validation → API call → structured output
   - **Key Concept**: Tool abstraction and error handling

5. **`tools/code_runner.py`** (80 lines)
   - Study `execute_code()` - subprocess management
   - Security: timeout, isolated process, no network
   - **Key Concept**: Safe execution of untrusted code

#### Memory Systems
6. **`memory/short_term.py`** (60 lines)
   - Sliding window with `deque` - O(1) append/pop
   - **Key Concept**: Context management with bounded memory

7. **`memory/long_term.py`** (100 lines)
   - Persistence pattern: load → operate → save
   - Simple retrieval (production would use embeddings)
   - **Key Concept**: Knowledge retention across sessions
   - **Note**: This demonstrates RAG principles - in production, replace keyword matching with vector embeddings (see section 6 & 8 above)

#### API & Infrastructure
8. **`api/main.py`** (200 lines)
   - REST endpoints: task creation, status, results
   - WebSocket: real-time updates
   - Async processing with `asyncio.create_task()`
   - **Key Concept**: Asynchronous request handling

9. **`docker-compose.yml`** (60 lines)
   - Service definitions and relationships
   - Volume mounts for data sharing
   - Health checks and dependencies
   - **Key Concept**: Multi-container orchestration

### Learning Path by Experience Level

#### Beginner (New to AI/LLMs)
1. Run the system and observe behavior
2. Read `agents/researcher.py` - simplest agent
3. Modify a system prompt in any agent
4. Add a new example in `examples/`

**Focus**: How LLMs use tools, basic agent patterns

#### Intermediate (Know Python, Basic AI)
1. Read `agents/base_agent.py` completely
2. Implement a new tool in `tools/`
3. Create a new specialized agent
4. Study the orchestrator's coordination logic

**Focus**: Reasoning loops, tool calling, multi-agent systems

#### Advanced (Want to Extend/Productionize)
1. Study the full orchestrator implementation
2. Implement parallel agent execution
3. Add vector-based memory with ChromaDB
4. Implement streaming responses
5. Add observability/telemetry

**Focus**: Scalability, production patterns, distributed systems

### Key Files to Study by Concept

**Agentic AI Patterns:**
- `agents/base_agent.py` - Agent reasoning loop
- `agents/orchestrator.py` - Multi-agent coordination
- `agents/planner.py` - Task decomposition

**LLM Integration:**
- `agents/base_agent.py` (line 40-55) - LLM calling
- `agents/*/get_system_prompt()` - Prompt engineering
- `agents/base_agent.py` (line 60-80) - Parsing LLM outputs

**Tool Use & APIs:**
- `tools/web_search.py` - External API integration
- `tools/code_runner.py` - Process execution
- `agents/base_agent.py` (line 85-100) - Tool execution

**Async & Concurrency:**
- `api/main.py` (line 50-80) - Async endpoints
- `api/main.py` (line 150-180) - WebSocket handling
- `api/main.py` (line 90-120) - Background task processing

**Containerization:**
- `docker-compose.yml` - Service orchestration
- `Dockerfile` - Application container
- `Dockerfile.sandbox` - Isolated execution environment

### Experiment Ideas

**Beginner Projects:**
1. **Add a New Agent**: Create `agents/translator.py` that translates text
2. **Add a New Tool**: Implement `tools/weather_api.py` for weather lookups
3. **Modify Prompts**: Improve system prompts with few-shot examples
4. **Custom Workflow**: Create a specialized workflow for code review

**Intermediate Projects:**
5. **Implement Vector RAG**: Replace keyword search in `memory/long_term.py` with sentence-transformers embeddings
   ```python
   # Use the code from section 8 above
   # Add ChromaDB for vector storage
   # Implement semantic similarity retrieval
   ```

6. **Add Streaming Responses**: Stream LLM outputs token-by-token to UI
7. **Parallel Execution**: Modify orchestrator to run independent agents concurrently
8. **Add Observability**: Log execution times, token usage, success rates with metrics/traces

**Advanced Projects:**
9. **Full RAG Pipeline**: Implement document chunking, embedding storage, and retrieval
   - Add PDF/document parsing
   - Chunk text intelligently (sliding window, semantic boundaries)
   - Store in vector DB with metadata
   - Retrieve relevant chunks before generation

10. **Implement Self-Reflection**: Add a "critic" agent that reviews and improves outputs
    ```python
    # After agent completes task:
    critique = critic_agent.evaluate(result)
    if critique.needs_improvement:
        improved = original_agent.refine(result, critique)
    ```

11. **Multi-Modal Agents**: Add image processing capabilities
    - Tool for image analysis (OCR, object detection)
    - Vision-language model integration

12. **Agent Learning**: Implement reinforcement learning from human feedback (RLHF)
    - Store successful strategies
    - Learn from corrections
    - Improve over time

### Understanding Design Patterns

**Strategy Pattern**: Different agents (strategies) for different tasks
- `agents/researcher.py`, `agents/analyst.py`, etc.
- All implement same interface (`BaseAgent`)
- Orchestrator selects appropriate strategy

**Template Method**: `BaseAgent.think()` defines algorithm structure
- Subclasses override `get_system_prompt()` and `get_available_tools()`
- Core reasoning loop stays consistent

**Observer Pattern**: WebSocket updates notify UI of changes
- `api/main.py` - observers (WebSocket connections)
- Task processing triggers notifications

**Command Pattern**: Tool calls as commands
- Tool schema defines interface
- Execution separated from invocation
- Easy to add new commands (tools)

## Learning Resources

### Documentation
- `docs/ARCHITECTURE.md` - Detailed system design and data flow
- `docs/EXAMPLES.md` - Extended use cases and tutorials
- `docs/GETTING_STARTED.md` - Setup and troubleshooting
- `COMPARISON.md` - vs simpler approaches

### Code Comments
All modules include docstrings explaining:
- Purpose and responsibilities
- Key methods and their algorithms
- Design decisions and trade-offs

### External Resources

**Foundational Papers & Concepts:**
- **ReAct (Reason + Act)**: "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
  - Paper demonstrating the reasoning-action loop implemented in this project
- **Chain-of-Thought**: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (Wei et al., 2022)
  - Shows how to make LLM reasoning explicit
- **RAG**: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (Lewis et al., 2020)
  - Foundational paper on combining retrieval with generation
- **Tool Use**: "Toolformer: Language Models Can Teach Themselves to Use Tools" (Schick et al., 2023)
  - Self-supervised learning of tool use

**Production Frameworks (similar patterns):**
- **LangChain**: Popular framework for LLM applications with agents, tools, memory
- **LlamaIndex**: Focuses on RAG and data ingestion pipelines
- **AutoGPT/BabyAGI**: Early autonomous agent implementations
- **CrewAI**: Multi-agent orchestration framework

**Vector Databases & Embeddings:**
- **ChromaDB**: Open-source embedding database (referenced in requirements.txt)
- **Sentence-Transformers**: Easy-to-use embedding models
- **FAISS**: Facebook's similarity search library (high-performance)
- **Pinecone/Weaviate**: Managed vector database services

**LLM & Agent Resources:**
- **OpenAI Function Calling**: Official documentation on tool use
- **Anthropic Claude**: Structured outputs and tool use
- **Ollama**: Local LLM hosting (used in this project)
- **HuggingFace**: Pre-trained models and embeddings

**Academic Resources:**
- Multi-agent systems literature (distributed AI)
- Reinforcement learning (agent training)
- Information retrieval (search and ranking)
- Natural language processing (text understanding)

## Contributing

This is a demo project for learning agentic AI patterns. Feel free to:
- Add new agent types
- Implement additional tools
- Improve the UI
- Add more example scenarios

## License

MIT License - Free for educational and commercial use

---

Built to demonstrate modern agentic AI principles

