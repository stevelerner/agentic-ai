# Simple Agentic AI Demo

A practical demonstration of core agentic AI principles that you can understand and run in 10 minutes.

**Learn by doing:** Single Python file, minimal setup, clear concepts.

## What You'll Learn

Three fundamental concepts that power modern AI agents:

### 1. Agent Reasoning Loop (ReAct Pattern)

```
Think → Act → Observe → Think → Act → ...
```

The agent:
- Decides what to do next (reasoning)
- Uses tools when needed (acting)
- Processes results (observing)
- Continues until task complete

### 2. Tool Use / Function Calling

```python
# Agent thinks: "I need to calculate this"
{"tool": "calculate", "arguments": {"expression": "25 * 4"}}

# Tool executes → returns result
{"result": 100.0}

# Agent continues with the result
"The answer is 100..."
```

The agent decides WHEN to use tools (not hardcoded). This extends LLMs beyond text generation.

### 3. LLM Integration

- Uses Ollama (local, no API costs)
- Maintains conversation context
- Iterative problem solving

## Quick Start (5 Minutes)

```bash
cd /Volumes/external/code/agentic-ai

# One command setup and run
./run-simple.sh
```

Or step by step:

```bash
# 1. Start Ollama
docker compose -f docker-compose-simple.yml up -d

# 2. Pull model (one-time, ~4GB)
docker exec simple-ollama ollama pull llama3.1

# 3. Install Python deps
pip3 install -r simple-requirements.txt

# 4. Run the agent
python3 simple-agent.py
```

## Example Interaction

```
You: Calculate (25 * 4) + (100 / 2) and save the result to result.txt

--- Iteration 1 ---
💭 Agent thinking: I need to calculate this expression first...
🧮 Tool: calculate(expression='(25 * 4) + (100 / 2)')
📊 Tool result: {"result": 150.0}

--- Iteration 2 ---
💭 Agent thinking: Now I'll save this to a file...
💾 Tool: save_file(filename='result.txt', content='Result: 150.0')
📊 Tool result: {"status": "success"}

✅ Final Answer:
I calculated the result as 150.0 and saved it to result.txt
```

The agent autonomously:
1. Broke down the task
2. Used calculator tool
3. Used file-save tool
4. Provided final answer

## How It Works

### The ReAct Loop

**File:** `simple-agent.py` (lines 100-150)

```python
def run(self, user_query: str):
    messages = [system_prompt, user_query]
    
    for iteration in range(max_iterations):
        # 1. REASONING: What should I do?
        response = call_llm(messages)
        
        # 2. Check if agent wants to use a tool
        if is_tool_call(response):
            # 3. ACTING: Execute the tool
            result = execute_tool(response)
            
            # 4. OBSERVING: Add result to context
            messages.append(result)
            continue  # Loop again with new info
        
        # 5. DONE: Agent has final answer
        return response
```

This is the core of agentic behavior - autonomous decision making with feedback loops.

### Available Tools

**File:** `simple-agent.py` (lines 15-60)

```python
def web_search(query: str, max_results: int = 3) -> list:
    """Search the web (mock results for demo)."""
    return search_results

def calculate(expression: str) -> float:
    """Evaluate math expressions safely."""
    return eval(expression)

def save_file(filename: str, content: str) -> dict:
    """Save content to a file."""
    with open(filename, 'w') as f:
        f.write(content)
    return {"status": "success"}
```

Tools are just Python functions. The agent decides when to call them.

### System Prompt

**File:** `simple-agent.py` (lines 120-135)

```python
system_prompt = """You are a helpful AI agent with access to tools.

Available tools:
- web_search(query, max_results): Search the web
- calculate(expression): Evaluate math expressions  
- save_file(filename, content): Save content to file

When you need to use a tool, respond with ONLY this JSON format:
{"tool": "tool_name", "arguments": {"arg1": "value1"}}

When you have enough information, provide your final answer without JSON.

Think step by step and use tools when needed."""
```

The prompt defines agent behavior and available capabilities.

## Understanding the Code

The entire implementation is in `simple-agent.py` (~200 lines). Key parts:

**Lines 15-60:** Tool definitions
```python
def your_tool(args):
    # Implementation
    return results
```

**Lines 80-180:** Agent class
```python
class SimpleAgent:
    def call_ollama()      # Talk to LLM
    def parse_tool_call()  # Extract JSON from response
    def execute_tool()     # Run the tool
    def run()              # Main ReAct loop
```

**Lines 200-250:** Example usage and interactive mode

The code is heavily commented - read it to understand exactly how it works!

## Extending the Agent

### Add a New Tool

```python
def weather(city: str) -> dict:
    """Get weather for a city."""
    # Your implementation (e.g., API call)
    return {"temp": 72, "condition": "sunny"}

# Register it
TOOLS["weather"] = {
    "function": weather,
    "description": "Get weather for a city",
    "parameters": {"city": "str"}
}
```

Then update the system prompt to tell the agent about the new tool. That's it!

### Improve Reliability

- **Lower temperature** (line 90): More consistent tool calling
- **Add examples** to system prompt (few-shot learning)
- **Better error handling** in tools
- **Validate tool outputs** before returning to agent

### Add Memory

```python
class SimpleAgent:
    def __init__(self):
        self.memory = []  # Store past interactions
    
    def run(self, query):
        # Retrieve relevant memories
        relevant = [m for m in self.memory if query in m]
        # Add to context
        messages.append({"role": "system", "content": str(relevant)})
```

## Files

- `simple-agent.py` - Complete implementation (200 lines)
- `docker-compose-simple.yml` - Just Ollama container
- `simple-requirements.txt` - One dependency: `requests`
- `SIMPLE-README.md` - Detailed documentation
- `run-simple.sh` - One-command setup

## Example Tasks to Try

After running `python3 simple-agent.py`, try:

```
Calculate 15 * 23 + 100

Search for information about ReAct pattern in AI

Calculate the area of a circle with radius 5 and save to area.txt

What is 2^10 + 2^20?
```

Watch how the agent breaks down tasks and uses tools appropriately.

## Troubleshooting

**Ollama not responding:**
```bash
docker logs simple-ollama
docker restart simple-ollama
```

**Model not found:**
```bash
docker exec simple-ollama ollama pull llama3.1
docker exec simple-ollama ollama list
```

**Agent not using tools correctly:**
- Check system prompt is clear
- Try lower temperature (0.1-0.3)
- Add examples of tool usage to prompt

**Web search returns mock data:**
- This is intentional for the demo
- To enable real search, uncomment the DuckDuckGo code in `simple-agent.py`

## What's Next?

Once you understand this simple agent:

1. **Experiment** - Try different queries, add tools
2. **Read the code** - It's short and well-commented
3. **Modify prompts** - See how behavior changes
4. **Build something** - Apply these patterns to your problem

### Advanced Concepts (Optional)

Want to explore more? See:

- **[README-ADVANCED.md](README-ADVANCED.md)** - Multi-agent orchestration system
- **[SIMPLE-README.md](SIMPLE-README.md)** - Extended documentation
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Deep technical dive

The advanced system adds:
- 5 specialized agents (Planner, Researcher, Analyst, Writer, Coder)
- Multi-agent orchestration
- Web UI with real-time updates
- RAG (Retrieval-Augmented Generation)
- Vector embeddings
- Production architecture

But start here first! Understanding this simple version makes everything else much clearer.

## Key Concepts Demonstrated

This simple demo teaches you:

**Agentic AI Fundamentals:**
- Autonomous decision making
- Tool use / function calling
- Iterative problem solving
- Context management

**Implementation Patterns:**
- Reasoning loops
- Structured outputs (JSON)
- LLM integration
- Error handling

**Computer Science:**
- State machines
- API design
- Process control
- Modular architecture

## Learning Path

```
Simple Demo (30 min)
    ↓
Understand code (1 hr)
    ↓
Add custom tools (1 hr)
    ↓
Modify for your use case (2+ hrs)
    ↓
Explore advanced system (optional)
```

## External Resources

**Papers to Read:**
- "ReAct: Synergizing Reasoning and Acting in Language Models" (Yao et al., 2022)
- "Chain-of-Thought Prompting" (Wei et al., 2022)

**Production Frameworks:**
- LangChain - Similar patterns at scale
- LlamaIndex - RAG-focused framework

## Contributing

This is a learning project. Improvements welcome:
- Better example tools
- Clearer documentation
- Additional examples
- Bug fixes

## License

MIT License - Free for educational and commercial use

---

**Get started:** Run `./run-simple.sh` and start exploring!

Questions? Read `SIMPLE-README.md` for more details or check out the advanced system in `README-ADVANCED.md`.
