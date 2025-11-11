#!/usr/bin/env python3
"""
Simple Agentic AI Demo - Single Agent with Tool Calling

Demonstrates core agentic AI concepts:
1. Agent reasoning loop (ReAct pattern)
2. Tool use / function calling
3. LLM integration (Ollama)
4. Iterative problem solving

Run: python3 simple-agent.py
"""

import json
import subprocess
from typing import Optional, Dict, Any
from dataclasses import dataclass


# ============================================================================
# TOOL DEFINITIONS
# ============================================================================

def web_search(query: str, max_results: int = 3) -> list:
    """
    Simulate web search (in real version, use DuckDuckGo API).
    For demo, returns mock results.
    """
    print(f"🔍 Tool: web_search(query='{query}', max_results={max_results})")
    
    # Mock results for demo
    results = [
        {"title": f"Result 1 about {query}", "url": "https://example.com/1", "snippet": f"Information about {query}..."},
        {"title": f"Result 2 about {query}", "url": "https://example.com/2", "snippet": f"More details on {query}..."},
        {"title": f"Result 3 about {query}", "url": "https://example.com/3", "snippet": f"Latest {query} updates..."},
    ]
    return results[:max_results]


def calculate(expression: str) -> float:
    """
    Safely evaluate mathematical expressions.
    """
    print(f"🧮 Tool: calculate(expression='{expression}')")
    try:
        # Safe evaluation - only allow numbers and basic operators
        allowed_chars = set('0123456789+-*/(). ')
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid characters in expression"}
        result = eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}


def save_file(filename: str, content: str) -> Dict[str, str]:
    """Save content to a file."""
    print(f"💾 Tool: save_file(filename='{filename}')")
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return {"status": "success", "message": f"Saved to {filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Available tools
TOOLS = {
    "web_search": {
        "function": web_search,
        "description": "Search the web for information",
        "parameters": {"query": "str", "max_results": "int (default 3)"}
    },
    "calculate": {
        "function": calculate,
        "description": "Evaluate a mathematical expression",
        "parameters": {"expression": "str"}
    },
    "save_file": {
        "function": save_file,
        "description": "Save content to a file",
        "parameters": {"filename": "str", "content": "str"}
    }
}


# ============================================================================
# AGENT CLASS
# ============================================================================

class SimpleAgent:
    """
    A simple agent that demonstrates the ReAct pattern:
    - Reasoning: Think about what to do
    - Acting: Use tools to accomplish tasks
    - Observing: Process tool results
    """
    
    def __init__(self, ollama_host: str = "http://localhost:11434"):
        self.ollama_host = ollama_host
        self.model = "llama3.1"
        self.conversation_history = []
        
    def call_ollama(self, messages: list) -> str:
        """Call Ollama API to get LLM response."""
        import requests
        
        try:
            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.2}
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Error calling Ollama: {e}\n\nMake sure Ollama is running: docker compose up -d ollama"
    
    def parse_tool_call(self, text: str) -> Optional[tuple]:
        """
        Try to extract a tool call from the LLM response.
        Expected format: {"tool": "tool_name", "arguments": {...}}
        """
        text = text.strip()
        
        # Look for JSON block
        if "{" in text and "}" in text:
            start = text.find("{")
            end = text.rfind("}") + 1
            json_str = text[start:end]
            
            try:
                obj = json.loads(json_str)
                if "tool" in obj and "arguments" in obj:
                    return obj["tool"], obj["arguments"]
            except:
                pass
        
        return None
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Execute a tool and return the result."""
        if tool_name not in TOOLS:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            tool_func = TOOLS[tool_name]["function"]
            result = tool_func(**arguments)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def run(self, user_query: str, max_iterations: int = 5) -> str:
        """
        Main agent loop implementing ReAct pattern:
        1. Reason about the task
        2. Decide on action (tool use or final answer)
        3. Observe results
        4. Repeat until task complete
        """
        
        # System prompt defines agent behavior
        system_prompt = """You are a helpful AI agent with access to tools.

Available tools:
- web_search(query, max_results): Search the web
- calculate(expression): Evaluate math expressions
- save_file(filename, content): Save content to a file

When you need to use a tool, respond with ONLY this JSON format:
{"tool": "tool_name", "arguments": {"arg1": "value1", "arg2": "value2"}}

When you have enough information to answer, provide your final answer without JSON.

Think step by step and use tools when needed."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        print(f"\n{'='*70}")
        print(f"🤖 Agent Task: {user_query}")
        print(f"{'='*70}\n")
        
        for iteration in range(1, max_iterations + 1):
            print(f"--- Iteration {iteration} ---")
            
            # REASONING: Get LLM response
            response = self.call_ollama(messages)
            print(f"💭 Agent thinking: {response[:200]}{'...' if len(response) > 200 else ''}\n")
            
            # Check if it's a tool call
            tool_call = self.parse_tool_call(response)
            
            if tool_call:
                # ACTING: Execute the tool
                tool_name, arguments = tool_call
                result = self.execute_tool(tool_name, arguments)
                
                # OBSERVING: Add tool result to conversation
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user", 
                    "content": f"Tool result: {json.dumps(result, indent=2)}"
                })
                
                print(f"📊 Tool result: {json.dumps(result, indent=2)}\n")
                
            else:
                # Final answer - no more tool calls
                print(f"{'='*70}")
                print(f"✅ Final Answer:")
                print(f"{'='*70}")
                print(response)
                print(f"{'='*70}\n")
                return response
        
        return "Maximum iterations reached. Task may be incomplete."


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def main():
    """Run example tasks to demonstrate the agent."""
    
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║                    Simple Agentic AI Demo                            ║
║                                                                      ║
║  Demonstrates: ReAct pattern, tool calling, reasoning loops         ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Create agent
    agent = SimpleAgent()
    
    # Example 1: Math calculation
    print("\n📝 EXAMPLE 1: Mathematical Reasoning\n")
    agent.run("Calculate (25 * 4) + (100 / 2) and explain the result")
    
    # Example 2: Information gathering
    print("\n📝 EXAMPLE 2: Information Gathering\n")
    agent.run("Search for information about agentic AI and summarize the key concepts")
    
    # Example 3: Multi-step task
    print("\n📝 EXAMPLE 3: Multi-step Task\n")
    agent.run("Calculate 123 * 456, then save the result to a file called result.txt")
    
    # Interactive mode
    print("\n" + "="*70)
    print("💬 Interactive Mode - Enter your queries (or 'quit' to exit)")
    print("="*70 + "\n")
    
    while True:
        try:
            query = input("You: ").strip()
            if query.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!\n")
                break
            if not query:
                continue
            
            agent.run(query)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()

