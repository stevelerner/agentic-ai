# Architecture Overview

This document explains the design and architecture of the Agentic AI demonstration system.

## System Architecture

```
┌─────────────┐
│   Web UI    │ (Nginx + Static HTML/JS)
│  (Port 80)  │
└──────┬──────┘
       │ HTTP/WebSocket
       ↓
┌─────────────────────────────────────┐
│      FastAPI Backend                │
│     (Orchestrator Service)          │
│         (Port 8000)                 │
│                                     │
│  ┌──────────────────────────────┐  │
│  │     Orchestrator             │  │
│  │   (Multi-Agent Coordinator)  │  │
│  └──────────┬───────────────────┘  │
│             │                       │
│    ┌────────┴────────┐             │
│    │                 │             │
│  ┌─▼──┐  ┌──▼──┐  ┌─▼───┐        │
│  │Plan│  │Res. │  │Anly.│  ...   │
│  │ner │  │     │  │     │         │
│  └────┘  └─────┘  └─────┘         │
│                                     │
│  ┌──────────────────────────────┐  │
│  │         Tools                │  │
│  │  ┌────────┬────────┬──────┐ │  │
│  │  │Search  │Files   │Code  │ │  │
│  │  └────────┴────────┴──────┘ │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │         Memory               │  │
│  │  ┌────────┬──────────────┐  │  │
│  │  │Short   │Long-term     │  │  │
│  │  │Term    │(Vector DB)   │  │  │
│  │  └────────┴──────────────┘  │  │
│  └──────────────────────────────┘  │
└───────────┬─────────────────────────┘
            │
            │ HTTP
            ↓
    ┌───────────────┐
    │    Ollama     │ (LLM Server)
    │ (Port 11434)  │
    │               │
    │  llama3.1     │
    └───────────────┘
```

## Core Components

### 1. Orchestrator

**Purpose:** Coordinates multiple specialized agents to accomplish complex tasks.

**Key Responsibilities:**
- Receives user queries
- Delegates to Planner for task decomposition
- Routes sub-tasks to appropriate specialist agents
- Manages execution flow and dependencies
- Synthesizes final results
- Handles errors and retries

**Design Pattern:** Orchestration (vs. Choreography)
- Central coordinator with explicit control flow
- Clear task delegation
- Dependency management
- Result aggregation

### 2. Specialized Agents

Each agent has:
- **Domain expertise** (system prompt)
- **Specific tools** (web search, file ops, code execution)
- **Reasoning loop** (can use tools iteratively)
- **Memory** (conversation history)

#### 2.1 Planner Agent

**Role:** Strategic planning and task decomposition

**Capabilities:**
- Break complex tasks into steps
- Identify required agents
- Determine dependencies
- Create execution plans

**Output:** Structured plan (JSON) with steps, agents, and dependencies

#### 2.2 Researcher Agent

**Role:** Information gathering and research

**Tools:**
- Web search (DuckDuckGo)
- News search
- Source validation

**Output:** Research findings with citations

#### 2.3 Analyst Agent

**Role:** Data analysis and synthesis

**Tools:**
- Data analysis
- Summarization
- Pattern recognition

**Output:** Insights, trends, recommendations

#### 2.4 Writer Agent

**Role:** Content creation and documentation

**Tools:**
- File operations (read/write)
- Markdown formatting

**Output:** Reports, documentation, articles

#### 2.5 Coder Agent

**Role:** Code generation and analysis

**Tools:**
- Code execution (sandbox)
- File operations
- Code validation

**Output:** Code, tests, documentation

### 3. Base Agent Architecture

All agents inherit from `BaseAgent`:

```python
class BaseAgent:
    - name: Agent identifier
    - role: Domain description
    - model: LLM model name
    - conversation_history: Short-term memory
    
    Methods:
    - think(): Main reasoning loop
    - call_llm(): LLM inference
    - parse_tool_call(): Extract tool calls from LLM response
    - execute_tool(): Run a tool and return results
    - get_system_prompt(): Define agent's behavior
    - get_available_tools(): List agent's tools
```

**Reasoning Loop:**

1. Receive user message
2. Call LLM with system prompt + history + message
3. Parse response
4. If tool call detected:
   - Execute tool
   - Add result to history
   - Go to step 2
5. If final answer:
   - Return response
   - Update history

**Max Iterations:** 5 (prevents infinite loops)

### 4. Tool System

**Design:** Tools are Python functions with metadata

```python
{
    "tool_name": {
        "description": "What the tool does",
        "function": callable,
        "parameters": {
            "param1": "type - description",
            ...
        }
    }
}
```

**Tool Calling Protocol:**

LLM responds with JSON:
```json
{
    "tool": "tool_name",
    "arguments": {
        "param1": "value1",
        ...
    }
}
```

**Available Tools:**

| Tool | Agent(s) | Purpose |
|------|----------|---------|
| web_search | Researcher | Search web via DuckDuckGo |
| analyze_data | Analyst | Process structured data |
| create_summary | Analyst | Summarize text |
| save_file | Writer, Coder | Save content to disk |
| read_file | Writer, Coder | Read file contents |
| execute_code | Coder | Run code in sandbox |

### 5. Memory System

#### 5.1 Short-Term Memory

**Purpose:** Conversation context within a session

**Implementation:** Sliding window (last N messages)

**Storage:** In-memory deque

**Use Cases:**
- Maintain conversation flow
- Reference recent context
- Support follow-up questions

#### 5.2 Long-Term Memory

**Purpose:** Persistent knowledge across sessions

**Implementation:** JSON storage (production would use vector DB like ChromaDB)

**Features:**
- Store task results
- Retrieve relevant memories
- Query by similarity (simplified keyword matching)

**Use Cases:**
- Learn from past tasks
- Avoid redundant work
- Build knowledge base

### 6. API Layer (FastAPI)

**Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/task` | POST | Submit new task |
| `/api/task/{id}` | GET | Get task status |
| `/api/tasks` | GET | List recent tasks |
| `/api/agents/status` | GET | Check agent health |
| `/api/memory/short-term` | GET | View conversation |
| `/api/memory/long-term` | GET | Memory stats |
| `/api/orchestrator/reset` | POST | Reset state |
| `/ws` | WebSocket | Real-time updates |

**Task Processing:**

1. User submits task via POST
2. Task ID generated and queued
3. Async processing starts
4. Status updates via WebSocket
5. Results stored and returned

**Concurrency:** Currently single-threaded (one task at a time)

### 7. Web UI

**Stack:** Vanilla JavaScript (no frameworks)

**Components:**
- Chat interface (center)
- Agent status panel (left)
- Execution details panel (right)

**Features:**
- Real-time updates (WebSocket)
- Markdown rendering
- Syntax highlighting
- Example prompts
- Execution log visualization
- Plan visualization

**Communication:**
- HTTP REST for task submission
- WebSocket for live updates
- Polling for task results

### 8. LLM Integration (Ollama)

**Why Ollama:**
- Runs locally (privacy)
- Easy model management
- Good performance
- Compatible with many models

**Model:** llama3.1 (default)
- Instruction-tuned
- Good reasoning capabilities
- Tool calling support
- ~4GB size

**Configuration:**
- Temperature: 0.2 (focused responses)
- Max tokens: 2000
- Host: Docker internal network

## Data Flow

### Example: Research Task

```
User: "Research AI agents and write a report"
  ↓
[Web UI] → POST /api/task
  ↓
[API] → Create task_id, queue task
  ↓
[Orchestrator] → Receive task
  ↓
[Planner] → Create execution plan
  ↓ Plan: Step 1 (researcher), Step 2 (analyst), Step 3 (writer)
  ↓
[Orchestrator] → Execute Step 1
  ↓
[Researcher] → "Search for AI agent papers"
  ↓
[Researcher] → Call web_search tool
  ↓
[web_search] → Query DuckDuckGo
  ↓
[DuckDuckGo] → Return results
  ↓
[Researcher] → Synthesize findings
  ↓
[Orchestrator] → Execute Step 2 (with Step 1 results)
  ↓
[Analyst] → Analyze research findings
  ↓
[Analyst] → Identify trends
  ↓
[Orchestrator] → Execute Step 3 (with Step 1 & 2 results)
  ↓
[Writer] → Create report
  ↓
[Writer] → Format as markdown
  ↓
[Writer] → Call save_file tool
  ↓
[Orchestrator] → Synthesize final result
  ↓
[API] → Store result
  ↓
[WebSocket] → Notify UI: "completed"
  ↓
[Web UI] → Display result
```

## Design Principles

### 1. Modularity

- Each agent is independent
- Tools are reusable
- Clear interfaces

### 2. Extensibility

- Easy to add new agents
- Easy to add new tools
- Minimal changes to core

### 3. Observability

- Rich logging
- Execution traces
- WebSocket updates

### 4. Fault Tolerance

- Tool call errors don't crash agents
- Max iteration limits
- Graceful degradation

### 5. Simplicity

- No complex frameworks
- Clear code structure
- Minimal dependencies

## Scalability Considerations

**Current Limitations:**
- Single-threaded task processing
- In-memory state
- No distributed execution

**Future Improvements:**
- Task queue (Celery, Redis)
- Distributed agents
- Vector database for memory
- Model caching
- Concurrent task processing

## Security

**Current Measures:**
- Code execution in sandbox
- Limited file system access
- No external API keys exposed
- Local LLM (no data sent out)

**Production Needs:**
- Authentication
- Rate limiting
- Input validation
- Sandboxing hardening
- Network isolation

## Performance

**Bottlenecks:**
- LLM inference (10-60s per call)
- Web search latency (1-3s)
- Multiple LLM calls per task

**Optimizations:**
- Streaming responses
- Parallel agent execution
- Model quantization
- Response caching

## Testing Strategy

**Unit Tests:**
- Individual agent logic
- Tool functionality
- Memory operations

**Integration Tests:**
- Orchestrator → Agent flow
- API endpoints
- WebSocket communication

**End-to-End Tests:**
- Complete task execution
- Example scenarios
- Error handling

---

This architecture demonstrates core agentic AI principles while remaining accessible and educational.

