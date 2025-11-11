# Advanced Multi-Agent Orchestration System

This is the advanced version with multiple specialized agents, orchestration, web UI, and production patterns.

**Prerequisites:** Understanding of the [simple demo](README.md) concepts.

## Overview

A production-quality multi-agent system demonstrating:

- **Multi-agent collaboration** (5 specialized agents)
- **Task planning and decomposition**
- **Complex tool orchestration**
- **Memory systems (short and long-term)**
- **Real-time web UI**
- **Production architecture patterns**

## Core AI & Computer Science Principles

This advanced demo implements and demonstrates 14 fundamental concepts:

**AI/ML Concepts:**
- Agent Architecture & Reasoning Loops
- Multi-Agent Systems & Orchestration  
- Tool Use & Function Calling
- Planning & Task Decomposition
- Memory Systems & Context Management
- RAG (Retrieval-Augmented Generation)
- Chain-of-Thought (CoT) & ReAct Pattern
- Embeddings & Vector Similarity
- Prompt Engineering

**Computer Science Concepts:**
- Asynchronous Task Processing
- Sandboxed Code Execution
- REST API & Service Architecture
- Real-Time Communication (WebSockets)
- Containerization & Orchestration

Each principle includes: concept definition, implementation location, code examples, and underlying CS theory.

## Architecture Overview

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
Final Output
```

## Quick Start

**Prerequisites:**
- Docker Desktop running
- 8GB+ RAM available
- Internet connection

**Setup:**
```bash
cd /Volumes/external/code/agentic-ai

# Build containers
docker compose build

# Start Ollama and pull model
docker compose up -d ollama
docker compose exec ollama ollama pull llama3.1

# Start all services
docker compose up -d

# Open web UI
open http://localhost:8080
```

**Or use Makefile:**
```bash
make setup  # One-time setup
make run    # Start system
```

## Project Structure

```
agentic-ai/
├── docker-compose.yml           ← Multi-service orchestration
├── Makefile                     ← Convenience commands
│
├── agents/                      ← 5 Specialized agents
│   ├── base_agent.py           ← Base agent class
│   ├── planner.py              ← Planning agent
│   ├── researcher.py           ← Research agent
│   ├── analyst.py              ← Analysis agent
│   ├── writer.py               ← Writing agent
│   ├── coder.py                ← Coding agent
│   └── orchestrator.py         ← Multi-agent coordinator
│
├── tools/                       ← Agent tools
│   ├── web_search.py           ← DuckDuckGo search
│   ├── file_ops.py             ← File operations
│   ├── code_runner.py          ← Safe code execution
│   └── data_tools.py           ← Data analysis
│
├── memory/                      ← Memory systems
│   ├── short_term.py           ← Conversation memory
│   └── long_term.py            ← Persistent memory
│
├── api/                         ← FastAPI backend
│   └── main.py                 ← API server
│
├── ui/                          ← Web interface
│   ├── index.html              ← Main UI
│   ├── app.js                  ← Frontend logic
│   └── styles.css              ← Styling
│
├── examples/                    ← Demo scenarios
│   ├── research_task.py
│   ├── analysis_task.py
│   └── coding_task.py
│
└── docs/                        ← Documentation
    ├── ARCHITECTURE.md
    ├── EXAMPLES.md
    └── GETTING_STARTED.md
```

## Example Use Cases

**1. Research & Report Generation**
```
Task: "Research the latest trends in AI agents and write a comprehensive 
       report with sources, analysis, and future predictions"

Flow:
  Planner → Creates multi-step plan
  Researcher → Searches web for recent articles
  Analyst → Synthesizes findings and identifies trends
  Writer → Generates structured report with citations
```

**2. Code Generation with Research**
```
Task: "Research best practices for REST APIs in Python and generate 
       a production-ready implementation with tests"

Flow:
  Researcher → Finds current best practices
  Planner → Designs API architecture
  Coder → Generates implementation code
  Coder → Writes comprehensive tests
  Writer → Creates documentation
```

## Key Concepts Deep Dive

### 1. Agent Architecture & Reasoning Loops

**Concept**: Autonomous agents that perceive, reason, and act iteratively.

**Implementation**: `agents/base_agent.py`

```python
def think(self, user_message: str) -> str:
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

**Concept**: Multiple specialized agents coordinate to solve complex problems.

**Implementation**: `agents/orchestrator.py`

```python
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

**Concept**: LLMs augmented with external tools/APIs.

**Implementation**: `agents/base_agent.py` + `tools/`

```python
# Tool definition pattern
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

**Concept**: Agents maintain context across interactions.

**Implementation**: `memory/short_term.py` + `memory/long_term.py`

**Short-term Memory** (Conversation Context):
- Sliding window with `deque` - O(1) operations
- Keep last N messages within token limits

**Long-term Memory** (Persistent Knowledge):
- JSON-based persistence (production uses vector DB)
- Keyword-based search (production uses embeddings)

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

**Concept**: Enhance LLM responses by retrieving relevant information before generation.

**Implementation**: `memory/long_term.py` + agent tool use

**Tool-Based RAG** (Web Search):
```python
# Agent realizes it needs information
response = '{"tool": "web_search", "arguments": {"query": "AI trends 2024"}}'

# Retrieve relevant documents
search_results = web_search("AI trends 2024", max_results=5)

# Augment next LLM call with retrieved information
context = f"Search results: {search_results}"
final_response = llm(user_query + context)
```

**Memory-Based RAG**:
```python
# Retrieve relevant past experiences
relevant_past_tasks = long_term_memory.retrieve(current_query)
response = llm(query + relevant_past_tasks)  # Augmented generation
```

**RAG Pipeline**: Query → Retrieval → Augmentation → Generation

**Production Enhancement**: Replace keyword matching with vector embeddings (see `requirements-optional.txt`)

### 7. Chain-of-Thought (CoT) & ReAct Pattern

**Concept**: Make LLM reasoning explicit through step-by-step thought processes.

**Implementation**: Agent reasoning loops demonstrate ReAct (Reasoning + Acting)

```python
# agents/base_agent.py - implements ReAct pattern
def think(self, user_message: str) -> str:
    for iteration in range(max_iterations):
        # REASONING: LLM thinks about what to do
        response = self.call_llm(messages)
        
        # ACTION: Execute tool based on reasoning
        if tool_call := self.parse_tool_call(response):
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

**CS Principles**: State machines, iterative refinement, trace logging

### 8. Embeddings & Vector Similarity

**Concept**: Represent text as dense vectors where semantic similarity = geometric proximity.

**Current Implementation**: Simplified keyword matching in `memory/long_term.py`

**Production Pattern**:
```python
from sentence_transformers import SentenceTransformer
import numpy as np

class LongTermMemory:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embeddings = []  # Vector representations
        self.memories = []    # Original text
    
    def store(self, content: str):
        embedding = self.encoder.encode(content)  # 384-dim vector
        self.embeddings.append(embedding)
        self.memories.append(content)
    
    def retrieve(self, query: str, top_k: int = 5):
        query_embedding = self.encoder.encode(query)
        
        # Compute cosine similarity with all stored vectors
        similarities = []
        for i, mem_embedding in enumerate(self.embeddings):
            sim = np.dot(query_embedding, mem_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(mem_embedding)
            )
            similarities.append((sim, self.memories[i]))
        
        return sorted(similarities, reverse=True)[:top_k]
```

**Why Embeddings?**
- Semantic understanding: "car" and "automobile" have similar vectors
- Multilingual: Cross-language similarity
- Efficient: Vector operations are fast (SIMD, GPU-accelerated)
- Approximate: No need for exact keyword matches

**CS Principles**: Linear algebra, cosine similarity, nearest neighbor search

### 9. Prompt Engineering & System Prompts

**Implementation**: Each agent defines `get_system_prompt()`

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
"""
```

**Techniques Used**:
- Role definition
- Capability listing
- Output format specification
- Task decomposition
- Examples (few-shot learning)

**CS Principles**: Domain-specific languages, behavior specification

### 10. Asynchronous Task Processing

**Implementation**: `api/main.py`

```python
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

**Implementation**: `tools/code_runner.py` + Docker

```python
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

**Implementation**: `api/main.py` (FastAPI)

```python
@app.post("/api/task", response_model=TaskResponse)
async def create_task(request: TaskRequest):
    # Type validation via Pydantic
    # Async processing
    # Structured response
```

**CS Principles**: RESTful design, service-oriented architecture, API contracts

### 13. Real-Time Communication & WebSockets

**Implementation**: `api/main.py` + `ui/app.js`

```python
# Server
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

**Implementation**: `docker-compose.yml` + Dockerfiles

```yaml
services:
  ollama:           # LLM server
  orchestrator:     # Agent system
  sandbox:          # Code execution
  ui:               # Web interface
```

**CS Principles**: Containerization, service mesh, infrastructure as code

## Commands

```bash
# Setup
make setup              # Initial setup
make run                # Start all services

# Usage  
make cli                # Interactive CLI mode
make examples           # Run demo scenarios

# Monitoring
make logs               # View all logs
make status             # Check health

# Cleanup
make stop               # Stop services
make clean              # Remove containers
make clean-all          # Complete cleanup
```

## Using the System

### Via Web UI (Recommended)

1. Navigate to http://localhost:8080
2. Enter your task in the chat interface
3. Watch agents collaborate in real-time
4. View reasoning traces and tool calls
5. Download generated artifacts

### Via CLI

```bash
make cli

# Or directly:
docker compose exec orchestrator python cli.py
```

### Via API

```bash
# Submit a task
curl -X POST http://localhost:8000/api/task \
  -H "Content-Type: application/json" \
  -d '{"query": "Research AI safety and write a summary"}'

# Check task status
curl http://localhost:8000/api/task/{task_id}
```

API docs: http://localhost:8000/docs

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

## Optional: Vector Embeddings & RAG

The core system uses simplified keyword matching. To enable production RAG:

See `requirements-optional.txt` for:
- ChromaDB (vector database)
- Sentence-transformers (embeddings)
- Instructions for C++ build tools

## Documentation

- **docs/ARCHITECTURE.md** - Detailed system design and data flow
- **docs/EXAMPLES.md** - Extended use cases and tutorials
- **docs/GETTING_STARTED.md** - Setup and troubleshooting
- **COMPARISON.md** - vs simpler approaches

## External Resources

**Foundational Papers:**
- ReAct: "Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
- Chain-of-Thought: "Elicits Reasoning in Large Language Models" (Wei et al., 2022)
- RAG: "Retrieval-Augmented Generation" (Lewis et al., 2020)
- Toolformer: "Language Models Can Teach Themselves to Use Tools" (Schick et al., 2023)

**Production Frameworks:**
- LangChain - Popular framework for LLM applications
- LlamaIndex - Focuses on RAG pipelines
- CrewAI - Multi-agent orchestration

**Vector Databases:**
- ChromaDB - Open-source embedding database
- Pinecone/Weaviate - Managed services
- FAISS - Facebook's similarity search library

## Troubleshooting

See `docs/GETTING_STARTED.md` for:
- Docker issues
- Service startup problems
- Performance tuning
- Common errors

---

**Ready to try?** Start with the [simple demo](README.md) first, then come back here!

