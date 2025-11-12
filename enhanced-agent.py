#!/usr/bin/env python3
"""
Enhanced Agentic AI - Full Feature Implementation

Demonstrates:
- Enhanced Observability
- Memory & Context
- Planning & Reflection
- Tool Intelligence
- Advanced Patterns (RAG)
- Failure Handling
"""

import json
import inspect
import re
import time
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, asdict
from collections import deque


@dataclass
class ConversationTurn:
    """Store a single conversation turn."""
    timestamp: str
    query: str
    response: str
    tools_used: List[str]
    tokens: int


class EnhancedAgent:
    """
    Enhanced agent with full observability, memory, planning, and advanced features.
    """
    
    def __init__(self, ollama_host: str = "http://ollama:11434", temperature: float = 0.2):
        self.ollama_host = ollama_host
        self.model = "llama3.1"
        self.temperature = temperature
        self.conversation_history = deque(maxlen=10)  # Last 10 turns
        self.context_window = 8192  # llama3.1 context window
        
    def call_ollama(self, messages: list, extract_json: bool = False) -> Tuple[str, Dict]:
        """
        Call Ollama with enhanced metrics tracking.
        
        Args:
            messages: Conversation messages
            extract_json: If True, extract JSON from markdown code blocks
            
        Returns:
            (content, metrics) tuple
        """
        try:
            response = requests.post(
                f"{self.ollama_host}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": self.temperature}
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()
            
            content = data["message"]["content"]
            
            # Extract JSON from markdown if needed
            if extract_json and "```json" in content:
                match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
                if match:
                    content = match.group(1)
            
            # Enhanced metrics
            metrics = {
                "model": data.get("model", self.model),
                "prompt_tokens": data.get("prompt_eval_count", 0),
                "completion_tokens": data.get("eval_count", 0),
                "total_tokens": data.get("prompt_eval_count", 0) + data.get("eval_count", 0),
                "prompt_eval_duration_ms": round(data.get("prompt_eval_duration", 0) / 1_000_000, 2),
                "eval_duration_ms": round(data.get("eval_duration", 0) / 1_000_000, 2),
                "total_duration_ms": round(data.get("total_duration", 0) / 1_000_000, 2),
                "temperature": self.temperature,
                # Cost estimation (Ollama is free, but show what it would cost)
                "estimated_cost_usd": self._estimate_cost(
                    data.get("prompt_eval_count", 0),
                    data.get("eval_count", 0)
                ),
            }
            
            return content, metrics
        except Exception as e:
            return f"Error calling Ollama: {e}", {}
    
    def _estimate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Estimate cost if this were a paid API.
        Using GPT-3.5-Turbo pricing as reference: $0.0015/1K prompt, $0.002/1K completion
        """
        prompt_cost = (prompt_tokens / 1000) * 0.0015
        completion_cost = (completion_tokens / 1000) * 0.002
        return round(prompt_cost + completion_cost, 6)
    
    def create_plan(self, user_query: str, memory_context: str = "") -> Tuple[Dict, Dict]:
        """
        PLANNING PHASE: Agent creates a plan before acting.
        """
        planning_prompt = f"""Given this user query, create a step-by-step plan.

User Query: {user_query}

{f"Previous Context: {memory_context}" if memory_context else ""}

Respond with JSON:
{{
    "understanding": "What the user wants",
    "plan": ["Step 1", "Step 2", "Step 3"],
    "tools_needed": ["tool1", "tool2"],
    "confidence": 0.85,
    "potential_issues": ["issue1", "issue2"]
}}"""
        
        messages = [{"role": "user", "content": planning_prompt}]
        response, metrics = self.call_ollama(messages, extract_json=True)
        
        try:
            plan = json.loads(response)
            return plan, metrics
        except:
            # Fallback plan
            return {
                "understanding": user_query,
                "plan": ["Analyze query", "Select appropriate tool", "Execute and respond"],
                "tools_needed": [],
                "confidence": 0.5,
                "potential_issues": ["Unable to parse plan"]
            }, metrics
    
    def critique_step(self, action: str, result: Any, goal: str) -> Tuple[Dict, Dict]:
        """
        REFLECTION PHASE: Agent critiques its own actions.
        """
        critique_prompt = f"""Evaluate this action and its result:

Goal: {goal}
Action Taken: {action}
Result: {json.dumps(result, indent=2)}

Respond with JSON:
{{
    "success": true/false,
    "effectiveness": 0.8,
    "reasoning": "Why this worked or didn't work",
    "next_action": "What to do next",
    "should_retry": true/false,
    "alternative_approach": "Different strategy if this didn't work"
}}"""
        
        messages = [{"role": "user", "content": critique_prompt}]
        response, metrics = self.call_ollama(messages, extract_json=True)
        
        try:
            critique = json.loads(response)
            return critique, metrics
        except:
            return {
                "success": not ("error" in str(result).lower()),
                "effectiveness": 0.5,
                "reasoning": "Unable to evaluate",
                "next_action": "Continue",
                "should_retry": False,
                "alternative_approach": "None"
            }, metrics
    
    def select_tool_with_reasoning(self, query: str, plan: Dict, tools: Dict) -> Tuple[Optional[Dict], Dict]:
        """
        TOOL INTELLIGENCE: Select tool with explicit reasoning.
        """
        tool_descriptions = "\n".join([
            f"- {name}: {info['description']}" 
            for name, info in tools.items()
        ])
        
        selection_prompt = f"""Select the best tool for this task:

Query: {query}
Plan Context: {plan.get('understanding', 'N/A')}

Available Tools:
{tool_descriptions}

Respond with JSON:
{{
    "selected_tool": "tool_name or null",
    "reasoning": "Why this tool is best",
    "confidence": 0.9,
    "arguments": {{"arg1": "value1"}},
    "alternative_tools": ["tool2", "tool3"],
    "validation_concerns": ["concern1"]
}}

If no tool is needed, set selected_tool to null."""
        
        messages = [{"role": "user", "content": selection_prompt}]
        response, metrics = self.call_ollama(messages, extract_json=True)
        
        try:
            selection = json.loads(response)
            return selection, metrics
        except:
            return None, metrics
    
    def execute_tool_with_retry(self, tool_name: str, arguments: Dict, 
                                 tool_func: callable, max_retries: int = 3) -> Tuple[Any, Dict]:
        """
        FAILURE HANDLING: Execute tool with retry logic and error classification.
        """
        attempts = []
        
        for attempt in range(1, max_retries + 1):
            try:
                start_time = time.time()
                
                # Type conversion
                sig = inspect.signature(tool_func)
                converted_args = {}
                
                for arg_name, arg_value in arguments.items():
                    if arg_name in sig.parameters:
                        param = sig.parameters[arg_name]
                        expected_type = param.annotation
                        
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
                duration_ms = round((time.time() - start_time) * 1000, 2)
                
                attempts.append({
                    "attempt": attempt,
                    "status": "success",
                    "duration_ms": duration_ms
                })
                
                return result, {
                    "attempts": attempts,
                    "total_attempts": attempt,
                    "final_status": "success"
                }
                
            except Exception as e:
                error_type = self._classify_error(e)
                duration_ms = round((time.time() - start_time) * 1000, 2)
                
                attempts.append({
                    "attempt": attempt,
                    "status": "failed",
                    "error": str(e),
                    "error_type": error_type,
                    "duration_ms": duration_ms
                })
                
                # Decide if we should retry
                if not self._should_retry(error_type) or attempt == max_retries:
                    return {"error": str(e), "error_type": error_type}, {
                        "attempts": attempts,
                        "total_attempts": attempt,
                        "final_status": "failed"
                    }
                
                # Exponential backoff
                time.sleep(0.1 * (2 ** (attempt - 1)))
        
        return {"error": "Max retries exceeded"}, {
            "attempts": attempts,
            "total_attempts": max_retries,
            "final_status": "failed"
        }
    
    def _classify_error(self, error: Exception) -> str:
        """Classify error type for better handling."""
        error_str = str(error).lower()
        
        if "timeout" in error_str or "connection" in error_str:
            return "NETWORK_ERROR"
        elif "permission" in error_str or "access" in error_str:
            return "PERMISSION_ERROR"
        elif "argument" in error_str or "parameter" in error_str:
            return "INVALID_INPUT"
        elif "not found" in error_str or "does not exist" in error_str:
            return "NOT_FOUND"
        else:
            return "LOGIC_ERROR"
    
    def _should_retry(self, error_type: str) -> bool:
        """Determine if error type is retryable."""
        retryable = ["NETWORK_ERROR", "TIMEOUT_ERROR"]
        return error_type in retryable
    
    def calculate_context_usage(self, messages: List[Dict]) -> Dict:
        """Calculate context window usage."""
        # Rough estimation: ~4 chars per token
        total_chars = sum(len(json.dumps(msg)) for msg in messages)
        estimated_tokens = total_chars // 4
        usage_pct = (estimated_tokens / self.context_window) * 100
        
        return {
            "estimated_tokens": estimated_tokens,
            "context_window": self.context_window,
            "usage_percent": round(usage_pct, 1),
            "remaining_tokens": self.context_window - estimated_tokens
        }
    
    def add_to_memory(self, query: str, response: str, tools_used: List[str], tokens: int):
        """Add interaction to conversation memory."""
        self.conversation_history.append(ConversationTurn(
            timestamp=datetime.now().isoformat(),
            query=query,
            response=response[:200],  # Truncate for memory efficiency
            tools_used=tools_used,
            tokens=tokens
        ))
    
    def get_memory_context(self) -> str:
        """Get summary of recent conversation history."""
        if not self.conversation_history:
            return ""
        
        summary_parts = []
        for turn in list(self.conversation_history)[-3:]:  # Last 3 turns
            summary_parts.append(
                f"Q: {turn.query[:100]} | Tools: {', '.join(turn.tools_used) if turn.tools_used else 'None'}"
            )
        
        return " || ".join(summary_parts)
    
    def get_session_summary(self) -> Dict:
        """Get summary of entire session."""
        if not self.conversation_history:
            return {
                "total_queries": 0,
                "total_tokens": 0,
                "tools_used_count": {},
                "average_tokens_per_query": 0
            }
        
        tools_count = {}
        total_tokens = 0
        
        for turn in self.conversation_history:
            total_tokens += turn.tokens
            for tool in turn.tools_used:
                tools_count[tool] = tools_count.get(tool, 0) + 1
        
        return {
            "total_queries": len(self.conversation_history),
            "total_tokens": total_tokens,
            "tools_used_count": tools_count,
            "average_tokens_per_query": round(total_tokens / len(self.conversation_history), 1),
            "session_start": self.conversation_history[0].timestamp if self.conversation_history else None
        }

