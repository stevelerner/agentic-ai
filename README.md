# Simple Agentic AI Demo

A practical demonstration of core agentic AI principles with **enhanced observability** - see exactly what's happening under the hood.

**Current Features:**
- ✓ **ReAct Pattern**: Reason → Act → Observe loop with full visibility
- ✓ **Enhanced Observability**: Token breakdown (prompt vs completion), conversation history
- ✓ **Tool Intelligence**: Automatic type conversion, argument validation
- ✓ **Per-step Metrics**: Timing, tokens, model for every LLM call
- ✓ **Language Tools**: Translation, summarization, rewriting, file operations
- ✓ **Clean Web UI**: Collapsible sections, full transparency

**Learn by doing:** Run in 5 minutes, understand agentic AI through clear examples.

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

### The ReAct Loop: Why Multiple Steps?

The agent operates in an iterative **Reason → Act → Observe** loop. This is what makes it "agentic" - it can adapt, recover from errors, and try different strategies.

**File:** `simple-server.py` (lines 228-289)

```python
def run(self, user_query: str):
    messages = [system_prompt, user_query]
    
    for iteration in range(max_iterations):
        # 1. REASONING: What should I do next?
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

#### When Does It Iterate Multiple Times?

The agent keeps looping until:
- ✓ **LLM provides a final answer** (no tool call detected)
- ⏱️ **Max iterations reached** (safety limit: 5 by default)

#### Real Example: Error Recovery

Query: *"Summarize the US Constitution Preamble"*

- **Step 1**: Agent calls `summarize_text` but forgets `text` argument → Gets error
- **Step 2**: Agent sees the error, corrects itself, includes the text → Tool succeeds
- **Step 3**: Agent realizes the tool output wasn't helpful, tries different parameters
- **Step 4**: Still not working as expected
- **Step 5**: Agent gives up on the tool and writes answer manually

This self-correction and adaptive behavior is the **core value of agentic AI** - it doesn't just execute one command, it reasons through problems.

#### Why Is This Better Than Single-Step?

Traditional approach:
```
User → LLM → One response (if wrong, user must retry)
```

Agentic approach:
```
User → Agent → [Try tool] → [See result] → [Try again] → [Adapt] → Final answer
```

The agent can:
1. **Recover from mistakes** (Step 1 → Step 2)
2. **Try different strategies** (Steps 2-4)
3. **Fall back gracefully** (Step 5)
4. **Chain multiple tools** (translate, then save to file)

This is the essence of agentic behavior.

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

## Key Features Explained

### Enhanced Observability

**Token Breakdown**: Every step shows prompt vs completion tokens
```
Prompt Tokens: 145
Completion Tokens: 89  
Total: 234
```

**Full Conversation History**: Click to expand and see:
- Every message exchanged with the LLM
- Token counts per message (prompt + completion)
- Tool calls and results
- Complete message flow

**Per-Step Metrics**: Each action shows:
- LLM Time: How long the model took
- Tool Time: How long tool execution took
- Model: Which model was used (llama3.1)

### Tool Intelligence

**Automatic Type Conversion**: 
```python
# LLM generates: {"max_sentences": "2"}
# Agent converts: max_sentences = 2 (int)
```

**Error Handling**: Clear error messages when tools fail

**Argument Validation**: Ensures correct types before execution

### Code Transparency

Every step shows:
- **File**: `simple-server.py`
- **Line**: Exact line number where AI call happens
- **Function**: Call chain (e.g., `SimpleAgent.run() → call_ollama()`)
- **Narrative**: Plain English explanation of what happened

## Files

- `simple-server.py` - Agent + web server (~380 lines)
- `templates/index.html` - Web UI with observability features
- `docker-compose-simple.yml` - Ollama + Web containers
- `Dockerfile.simple` - Web service container
- `simple-requirements.txt` - Minimal dependencies (ollama, requests, Flask)
- `run-simple.sh` - One-command setup
- `cleanup-simple.sh` - Safe cleanup script

## Example Tasks to Try

Open **http://localhost:8000** and try:

```
Translate 'Hello, how are you?' to Spanish

Rewrite 'hey whats up' in a formal style

Summarize the US Constitution Preamble

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

## What You'll See

When you run a query, the UI shows:

1. **Each Step** - Collapsible sections for each iteration
2. **Tool Calls** - Arguments sent and results received
3. **Token Metrics** - Breakdown of every LLM call
4. **Timing** - How long each step took
5. **Code Context** - Where in the code each action happened
6. **Conversation History** - Full message exchange (expandable)

### Example: "Translate 'Hello' to Spanish"

**Step 1 - Tool Call:**
```
Tool: translate_text
Arguments: {"text": "Hello", "target_language": "Spanish"}
Result: {"translated": "[Spanish translation of: Hello]"}

Metrics:
- Prompt Tokens: 145
- Completion Tokens: 89
- Total: 234
- LLM Time: 2543ms
- Tool Time: 0.03ms
```

**Step 2 - Final Answer:**
```
The Spanish translation is: "Hola"

Summary:
- Total Tokens: 458
- Total Time: 4,832ms
- Iterations: 2
- Messages: 4
```

### Extending the Demo

**Add a new tool** (easy):
```python
def sentiment_analysis(text: str) -> dict:
    """Analyze sentiment of text."""
    # Your implementation
    return {"sentiment": "positive", "confidence": 0.85}

TOOLS["sentiment_analysis"] = {
    "function": sentiment_analysis,
    "description": "Analyze sentiment of text",
    "parameters": {"text": "str"}
}
```

**Adjust agent behavior**: Edit the system prompt in `simple-server.py` (line 205)

**Change temperature**: Modify `SimpleAgent.__init__()` to adjust creativity (default 0.2)

## Advanced Concepts (Optional)

For a more complex multi-agent system with planning, reflection, and RAG, see `README-ADVANCED.md`.

**This simple demo focuses on clarity and understanding. The advanced demo adds:**

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
