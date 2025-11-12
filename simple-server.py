#!/usr/bin/env python3
"""
Simple Agentic AI Demo - Web Server

Demonstrates core agentic AI concepts with a clean web interface.
"""

import json
import inspect
from typing import Optional, Dict, Any, List
from flask import Flask, render_template, request, jsonify, Response
import requests
import time

app = Flask(__name__)

# ============================================================================
# TOOL DEFINITIONS - Language focused
# ============================================================================

def translate_text(text: str, target_language: str = "Spanish") -> Dict:
    """
    Translate text to another language.
    For demo, returns mock translation (in production, use translation API).
    """
    print(f"🌍 Tool: translate_text(text='{text[:50]}...', target='{target_language}')")
    
    # Mock translations for demo
    translations = {
        "Spanish": f"[Spanish translation of: {text}]",
        "French": f"[French translation of: {text}]",
        "German": f"[German translation of: {text}]",
    }
    
    return {
        "original": text,
        "language": target_language,
        "translated": translations.get(target_language, f"[{target_language} translation of: {text}]")
    }


def summarize_text(text: str, max_sentences: int = 3) -> Dict:
    """
    Summarize a longer text into key points.
    """
    print(f"📝 Tool: summarize_text(text length={len(text)}, max_sentences={max_sentences})")
    
    # Simple mock summarization (in production, use proper summarization)
    sentences = text.split('.')[:max_sentences]
    summary = '. '.join(s.strip() for s in sentences if s.strip()) + '.'
    
    return {
        "original_length": len(text),
        "summary": summary,
        "compression_ratio": len(summary) / len(text) if text else 0
    }


def rewrite_text(text: str, style: str = "formal") -> Dict:
    """
    Rewrite text in a different style.
    """
    print(f"✍️ Tool: rewrite_text(text='{text[:50]}...', style='{style}')")
    
    return {
        "original": text,
        "style": style,
        "rewritten": f"[Text rewritten in {style} style: {text}]"
    }


def save_file(filename: str, content: str) -> Dict[str, str]:
    """Save content to a file."""
    print(f"💾 Tool: save_file(filename='{filename}')")
    try:
        with open(f"outputs/{filename}", 'w') as f:
            f.write(content)
        return {"status": "success", "message": f"Saved to outputs/{filename}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# Available tools
TOOLS = {
    "translate_text": {
        "function": translate_text,
        "description": "Translate text to another language",
        "parameters": {"text": "str", "target_language": "str (Spanish, French, German)"}
    },
    "summarize_text": {
        "function": summarize_text,
        "description": "Summarize longer text into key points",
        "parameters": {"text": "str", "max_sentences": "int (default 3)"}
    },
    "rewrite_text": {
        "function": rewrite_text,
        "description": "Rewrite text in a different style",
        "parameters": {"text": "str", "style": "str (formal, casual, technical)"}
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
    """Simple agent demonstrating ReAct pattern."""
    
    def __init__(self, ollama_host: str = "http://ollama:11434"):
        self.ollama_host = ollama_host
        self.model = "llama3.1"
        
    def call_ollama(self, messages: list) -> tuple:
        """Call Ollama API to get LLM response. Returns (content, metrics)."""
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
            data = response.json()
            
            # Enhanced metrics with cost estimation
            prompt_tokens = data.get("prompt_eval_count", 0)
            completion_tokens = data.get("eval_count", 0)
            
            metrics = {
                "model": data.get("model", self.model),
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
                "eval_duration_ms": round(data.get("eval_duration", 0) / 1_000_000, 2),
                "total_duration_ms": round(data.get("total_duration", 0) / 1_000_000, 2),
                "temperature": 0.2,
                # Cost estimation (GPT-3.5-Turbo pricing: $0.0015/1K prompt, $0.002/1K completion)
                "estimated_cost_usd": round(
                    (prompt_tokens / 1000) * 0.0015 + (completion_tokens / 1000) * 0.002, 
                    6
                ),
            }
            
            return data["message"]["content"], metrics
        except Exception as e:
            return f"Error calling Ollama: {e}", {}
    
    def parse_tool_call(self, text: str) -> Optional[tuple]:
        """Extract tool call from LLM response."""
        text = text.strip()
        
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
        """Execute a tool and return the result with proper type conversion."""
        if tool_name not in TOOLS:
            return {"error": f"Unknown tool: {tool_name}"}
        
        try:
            tool_func = TOOLS[tool_name]["function"]
            
            # Convert argument types to match function signature
            sig = inspect.signature(tool_func)
            converted_args = {}
            
            for arg_name, arg_value in arguments.items():
                if arg_name in sig.parameters:
                    param = sig.parameters[arg_name]
                    expected_type = param.annotation
                    
                    # Convert to expected type
                    if expected_type == int and not isinstance(arg_value, int):
                        converted_args[arg_name] = int(arg_value)
                    elif expected_type == float and not isinstance(arg_value, float):
                        converted_args[arg_name] = float(arg_value)
                    elif expected_type == bool and not isinstance(arg_value, bool):
                        converted_args[arg_name] = str(arg_value).lower() in ('true', '1', 'yes')
                    else:
                        converted_args[arg_name] = arg_value
                else:
                    converted_args[arg_name] = arg_value
            
            result = tool_func(**converted_args)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def run(self, user_query: str, max_iterations: int = 5) -> Dict:
        """
        Run agent with ReAct pattern, returning step-by-step trace with full observability.
        """
        system_prompt = """You are a helpful AI assistant specializing in language tasks.

Available tools:
- translate_text(text, target_language): Translate to Spanish, French, or German
- summarize_text(text, max_sentences): Create a concise summary
- rewrite_text(text, style): Rewrite in formal, casual, or technical style
- save_file(filename, content): Save content to a file

When you need to use a tool, respond with ONLY this JSON format:
{"tool": "tool_name", "arguments": {"arg1": "value1", "arg2": "value2"}}

When you have enough information to answer, provide your final answer without JSON.

Think step by step and use tools when helpful."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ]
        
        trace = []
        total_tokens = 0
        total_time_ms = 0
        total_cost = 0.0
        conversation_history = []  # Track full conversation
        
        for iteration in range(1, max_iterations + 1):
            # REASONING: Get LLM response with metrics
            response, metrics = self.call_ollama(messages)
            total_tokens += metrics.get("total_tokens", 0)
            total_time_ms += metrics.get("total_duration_ms", 0)
            total_cost += metrics.get("estimated_cost_usd", 0)
            
            # Track conversation
            conversation_history.append({
                "role": "assistant",
                "content": response,
                "tokens": metrics.get("total_tokens", 0),
                "prompt_tokens": metrics.get("prompt_tokens", 0),
                "completion_tokens": metrics.get("completion_tokens", 0)
            })
            
            # Check if it's a tool call
            tool_call = self.parse_tool_call(response)
            
            if tool_call:
                # ACTING: Execute the tool
                tool_name, arguments = tool_call
                tool_start = time.time()
                result = self.execute_tool(tool_name, arguments)
                tool_duration_ms = round((time.time() - tool_start) * 1000, 2)
                
                trace.append({
                    "type": "tool_call",
                    "iteration": iteration,
                    "tool": tool_name,
                    "arguments": arguments,
                    "result": result,
                    "llm_metrics": metrics,
                    "tool_duration_ms": tool_duration_ms,
                    "context": {
                        "phase": "ReAct Pattern: Reasoning → Acting",
                        "file": "simple-server.py",
                        "line": "230-242",
                        "function": "SimpleAgent.run() → call_ollama() → execute_tool()",
                        "narrative": f"Agent analyzed the query and decided to call {tool_name}. The LLM (line 230) generated a JSON tool call, which was parsed (line 235) and executed (line 242). Type conversion (line 175-195) ensures string arguments like '2' are converted to int 2. The tool result will be fed back to the LLM for the next reasoning step."
                    }
                })
                
                # OBSERVING: Add tool result to conversation
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user", 
                    "content": f"Tool result: {json.dumps(result, indent=2)}"
                })
                
                # Track tool result in conversation history
                conversation_history.append({
                    "role": "tool",
                    "tool": tool_name,
                    "content": result,
                    "tokens": 0
                })
                
            else:
                # Final answer
                trace.append({
                    "type": "final_answer",
                    "iteration": iteration,
                    "content": response,
                    "llm_metrics": metrics,
                    "summary": {
                        "total_tokens": total_tokens,
                        "total_time_ms": round(total_time_ms, 2),
                        "total_cost_usd": round(total_cost, 6),
                        "model": self.model,
                        "iterations": iteration,
                        "conversation_messages": len(messages)
                    },
                    "conversation_history": conversation_history,
                    "context": {
                        "phase": "ReAct Pattern: Final Response",
                        "file": "simple-server.py",
                        "line": "230",
                        "function": "SimpleAgent.run() → call_ollama()",
                        "narrative": f"Agent completed its reasoning loop after {iteration} iteration(s). The LLM determined it had sufficient information from tool results to provide a final answer to the user. Total conversation included {len(messages)} messages exchanged with the LLM."
                    }
                })
                return {"trace": trace}
        
        # Max iterations reached
        trace.append({
            "type": "final_answer",
            "iteration": max_iterations,
            "content": "Maximum iterations reached without completing the task.",
            "summary": {
                "total_tokens": total_tokens,
                "total_time_ms": round(total_time_ms, 2),
                "total_cost_usd": round(total_cost, 6),
                "model": self.model,
                "iterations": max_iterations,
                "conversation_messages": len(messages)
            },
            "conversation_history": conversation_history,
            "context": {
                "phase": "ReAct Pattern: Iteration Limit Reached",
                "file": "simple-server.py",
                "line": "228",
                "function": "SimpleAgent.run()",
                "narrative": f"Agent reached the maximum iteration limit of {max_iterations} steps. This safety mechanism prevents infinite loops. Consider increasing max_iterations or simplifying the query."
            }
        })
        return {"trace": trace}


# ============================================================================
# WEB ROUTES
# ============================================================================

agent = SimpleAgent()

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def handle_query():
    """Process a user query through the agent."""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    # Run agent and get result with full observability
    result = agent.run(query)
    
    return jsonify({
        "status": "success",
        "query": query,
        "trace": result["trace"]
    })

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Return example queries."""
    return jsonify({
        "examples": [
            "Translate 'Hello, how are you?' to Spanish",
            "Summarize this text: [paste long text here]",
            "Rewrite 'hey whats up' in a formal style",
            "Translate 'Good morning' to French and save it to greeting.txt",
            "Take this paragraph and make it more casual: [your text]"
        ]
    })

if __name__ == '__main__':
    import os
    os.makedirs('outputs', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

