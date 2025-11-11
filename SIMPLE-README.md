# Simple Agentic AI Demo

A minimal, working demonstration of core agentic AI principles.

## What This Demonstrates

1. **Agent Reasoning Loop (ReAct Pattern)**
   - Reasoning: Agent thinks about what to do
   - Acting: Agent uses tools to accomplish tasks  
   - Observing: Agent processes tool results
   - Iterating: Loop continues until task complete

2. **Tool Use / Function Calling**
   - Agent decides when to use tools
   - Structured output (JSON) for tool calls
   - Tools execute and return results
   - Results fed back to agent for next step

3. **LLM Integration**
   - Uses Ollama (local LLM)
   - No external API costs
   - Full conversation context maintained

## Quick Start (5 Minutes)

### Step 1: Start Ollama

```bash
# Start Ollama container
docker compose -f docker-compose-simple.yml up -d

# Pull the model (one-time, ~4GB)
docker exec simple-ollama ollama pull llama3.1
```

### Step 2: Install Python Dependencies

```bash
pip3 install -r simple-requirements.txt
```

### Step 3: Run the Agent

```bash
python3 simple-agent.py
```

That's it! The agent will run example tasks and then enter interactive mode.

## How It Works

### The ReAct Loop

```
User Query
    ↓
┌─────────────────────────────────┐
│  Agent Reasoning (LLM)          │
│  "What should I do next?"       │
└────────────┬────────────────────┘
             │
             ├──→ Need tool?  ──→ YES ──→ Execute Tool ──→ Observe Result ──┐
             │                                                                │
             └──→ Have answer? ──→ YES ──→ Return Final Answer              │
                                                                              │
                                                                              │
                     Loop back ←─────────────────────────────────────────────┘
```

### Code Structure

```python
# 1. Define tools
def web_search(query: str) -> list:
    # Tool implementation
    return results

# 2. Create agent
class SimpleAgent:
    def run(self, user_query: str):
        # ReAct loop
        for iteration in range(max_iterations):
            response = llm(query + history)
            
            if is_tool_call(response):
                result = execute_tool(response)
                history.append(result)
                # Continue loop
            else:
                return response  # Final answer

# 3. Use agent
agent = SimpleAgent()
agent.run("Calculate 25 * 4 and save to file.txt")
```

## Example Interactions

### Example 1: Math Calculation

```
You: Calculate (25 * 4) + (100 / 2)

Agent thinking: I need to calculate this expression...
🧮 Tool: calculate(expression='(25 * 4) + (100 / 2)')
Tool result: {"result": 150.0}

Final Answer: The result is 150. This comes from (25 * 4) = 100, plus (100 / 2) = 50.
```

### Example 2: Multi-step Task

```
You: Search for agentic AI info and save summary to notes.txt

Iteration 1:
Agent thinking: I'll search for information first...
🔍 Tool: web_search(query='agentic AI')
Tool result: [{"title": "What is Agentic AI", ...}]

Iteration 2:
Agent thinking: Now I'll create a summary and save it...
💾 Tool: save_file(filename='notes.txt', content='Summary: ...')
Tool result: {"status": "success"}

Final Answer: I've searched for agentic AI information and saved a summary to notes.txt
```

## Key Concepts Explained

### 1. Reasoning Loop

**Location**: `SimpleAgent.run()` method

The agent iterates through a reasoning process:
- Call LLM with current context
- Parse response (tool call or final answer?)
- If tool call: execute and continue
- If final answer: return to user

This is the core of agentic behavior - autonomous decision making with feedback loops.

### 2. Tool Calling

**Location**: `parse_tool_call()` and `execute_tool()` methods

Tools extend agent capabilities beyond text generation:
- Web search: Access current information
- Calculator: Perform computations
- File operations: Persist results

The agent decides WHEN to use tools (not hardcoded).

### 3. Structured Output

**Location**: System prompt in `run()` method

The LLM is prompted to output JSON for tool calls:
```json
{"tool": "calculate", "arguments": {"expression": "2+2"}}
```

This enables reliable parsing and tool execution.

### 4. Context Management

**Location**: `messages` list in `run()` method

The agent maintains conversation history:
- System prompt (defines behavior)
- User query
- Agent responses
- Tool results

This allows the agent to reason about previous steps.

## Extending the Agent

### Add a New Tool

```python
def your_tool(arg1: str, arg2: int) -> Any:
    """Tool description."""
    # Your implementation
    return result

# Register it
TOOLS["your_tool"] = {
    "function": your_tool,
    "description": "What your tool does",
    "parameters": {"arg1": "str", "arg2": "int"}
}
```

Update the system prompt to tell the agent about the new tool.

### Improve Tool Calling

Current implementation uses simple JSON parsing. For production:
- Use OpenAI function calling format
- Add JSON schema validation
- Handle partial/malformed JSON
- Support multiple tool calls in one response

### Add Memory

```python
class SimpleAgent:
    def __init__(self):
        self.long_term_memory = []  # Store past interactions
    
    def run(self, query):
        # Retrieve relevant memories
        relevant = self.search_memory(query)
        # Add to context
        messages.append({"role": "system", "content": f"Relevant past info: {relevant}"})
```

## Troubleshooting

### Ollama not responding

```bash
# Check if running
docker ps | grep ollama

# View logs
docker logs simple-ollama

# Restart
docker restart simple-ollama
```

### Model not found

```bash
# Pull the model
docker exec simple-ollama ollama pull llama3.1

# List available models
docker exec simple-ollama ollama list
```

### Agent not using tools

The LLM might not be following the JSON format. Try:
- Adjusting temperature (lower = more consistent)
- Improving system prompt
- Adding examples in prompt (few-shot learning)

## Comparison to Full System

This simple version focuses on core concepts:

| Feature | Simple Version | Full Version |
|---------|---------------|--------------|
| Agents | 1 generic | 5 specialized |
| Tools | 3 basic | 6+ advanced |
| Architecture | Single file | Modular system |
| UI | CLI only | Web + CLI + API |
| Containers | Just Ollama | 4 services |
| Memory | Conversation only | Short + long term |
| Orchestration | N/A | Multi-agent coordination |

**Start here**, understand the concepts, then explore the full system.

## Next Steps

1. **Experiment**: Try different queries, watch the reasoning
2. **Add Tools**: Implement weather API, database access, etc.
3. **Improve Prompts**: Make the agent more reliable
4. **Add Memory**: Store and retrieve past interactions
5. **Read Full Docs**: See `README.md` for advanced concepts

## Files

- `simple-agent.py` - Main agent implementation (200 lines)
- `docker-compose-simple.yml` - Just Ollama container
- `simple-requirements.txt` - Minimal dependencies
- `SIMPLE-README.md` - This file

## Learning Resources

- **ReAct Paper**: "ReAct: Synergizing Reasoning and Acting in Language Models"
- **Tool Use**: OpenAI function calling documentation
- **Prompt Engineering**: How to write effective system prompts
- **Full README**: Advanced concepts (RAG, embeddings, multi-agent)

---

Built to demonstrate core agentic AI principles simply and clearly.

