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

Then open your browser to: **http://localhost:8000**

Or step by step:

```bash
# 1. Start both containers (Ollama + Web UI)
docker compose -f docker-compose-simple.yml up -d --build

# 2. Pull model (one-time, ~4GB)
docker exec simple-ollama ollama pull llama3.1

# 3. Open browser
open http://localhost:8000
```

## Example Interaction

In the web interface, try:

**Query:** "Translate 'Hello, how are you?' to Spanish"

**Agent Process:**

**Step 1** - Tool Call:
```
Tool: translate_text
Arguments: {
  "text": "Hello, how are you?",
  "target_language": "Spanish"
}
Result: {
  "translated": "Hola, ¿cómo estás?"
}
```

**Step 2** - Final Answer:
```
The Spanish translation is: "Hola, ¿cómo estás?"
```

The agent autonomously:
1. Understood you wanted translation
2. Called the translate tool with correct arguments
3. Received the result
4. Provided a clear answer

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

### Available Tools (Language Focused)

**File:** `simple-server.py` (lines 15-80)

```python
def translate_text(text: str, target_language: str) -> dict:
    """Translate text to Spanish, French, or German."""
    return {"translated": translated_text}

def summarize_text(text: str, max_sentences: int = 3) -> dict:
    """Summarize longer text into key points."""
    return {"summary": summary_text}

def rewrite_text(text: str, style: str) -> dict:
    """Rewrite text in formal, casual, or technical style."""
    return {"rewritten": rewritten_text}

def save_file(filename: str, content: str) -> dict:
    """Save content to a file."""
    with open(f"outputs/{filename}", 'w') as f:
        f.write(content)
    return {"status": "success"}
```

Tools are just Python functions. The agent decides when and how to call them.

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

The implementation is in `simple-server.py` (~250 lines). Key parts:

**Lines 15-80:** Tool definitions (language-focused)
```python
def translate_text(text, target_language):
    # Translation implementation
    return result

def summarize_text(text, max_sentences):
    # Summarization implementation
    return result
```

**Lines 90-180:** Agent class
```python
class SimpleAgent:
    def call_ollama()      # Talk to LLM
    def parse_tool_call()  # Extract JSON from response
    def execute_tool()     # Run the tool
    def run()              # Main ReAct loop
```

**Lines 200-250:** Flask web server + API endpoints

The code is well-commented and the web UI makes it easy to see the agent in action!

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

- `simple-server.py` - Agent + web server (250 lines)
- `templates/index.html` - Web UI with metrics display
- `docker-compose-simple.yml` - Ollama + Web containers
- `Dockerfile.simple` - Web service container
- `simple-requirements.txt` - Minimal dependencies
- `SIMPLE-README.md` - Detailed documentation
- `run-simple.sh` - One-command setup
- `cleanup-simple.sh` - Safe cleanup script

## Example Tasks to Try

Open **http://localhost:8000** and try these language tasks:

```
Translate 'Good morning' to French

Rewrite 'hey whats up' in a formal style

Summarize this: [paste a long paragraph]

Translate 'Hello world' to Spanish and save it to greeting.txt

Make this more professional: 'wanna grab coffee l8r?'
```

Watch how the agent:
- Decides which tool to use
- Calls tools with correct arguments
- Processes results
- Provides clear answers

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

**Translation returns mock data:**
- This is intentional for the demo
- To enable real translation, integrate a translation API in `simple-server.py`

**Can't access localhost:8000:**
```bash
# Check containers are running
docker ps | grep simple

# Check logs
docker compose -f docker-compose-simple.yml logs web
```

## Cleanup

**Quick cleanup** (keeps Ollama and model):

```bash
./cleanup-simple.sh
```

**Manual cleanup** (same as script):

```bash
docker compose -f docker-compose-simple.yml down
```

**Nuclear cleanup** (removes everything including model):

```bash
docker compose -f docker-compose-simple.yml down -v
```

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

**Get started:** 

```bash
./run-simple.sh
```

Then open **http://localhost:8000** and watch the AI agent work!

Questions? Read `SIMPLE-README.md` for more details or check out the advanced system in `README-ADVANCED.md`.
