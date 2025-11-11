"""Base agent class with common functionality."""
import json
import ollama
from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod
from rich.console import Console

console = Console()


class BaseAgent(ABC):
    """Base class for all agents with common LLM and tool calling functionality."""
    
    def __init__(
        self,
        name: str,
        role: str,
        model: str = "llama3.1",
        temperature: float = 0.2,
        max_tokens: int = 2000
    ):
        self.name = name
        self.role = role
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.conversation_history: List[Dict[str, str]] = []
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the system prompt for this agent."""
        pass
    
    @abstractmethod
    def get_available_tools(self) -> Dict[str, Any]:
        """Return dict of tools available to this agent."""
        pass
    
    def call_llm(self, messages: List[Dict[str, str]]) -> str:
        """Call the LLM with messages."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            )
            return response["message"]["content"]
        except Exception as e:
            console.print(f"[red]LLM Error: {e}[/red]")
            return f"Error calling LLM: {str(e)}"
    
    def parse_tool_call(self, text: str) -> Optional[tuple[str, Dict[str, Any]]]:
        """Try to parse a tool call from LLM response."""
        text = text.strip()
        
        # Look for JSON object with "tool" and "arguments" keys
        if text.startswith("{") and text.endswith("}"):
            try:
                obj = json.loads(text)
                if "tool" in obj and "arguments" in obj:
                    return obj["tool"], obj["arguments"]
            except json.JSONDecodeError:
                pass
        
        # Look for function call format: tool_name(arg1=val1, arg2=val2)
        if "(" in text and ")" in text:
            try:
                tool_name = text.split("(")[0].strip()
                args_str = text.split("(")[1].split(")")[0]
                # Simple parsing - in production use proper parser
                args = {}
                if args_str:
                    for pair in args_str.split(","):
                        if "=" in pair:
                            k, v = pair.split("=", 1)
                            args[k.strip()] = v.strip().strip('"\'')
                return tool_name, args
            except Exception:
                pass
        
        return None
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute a tool and return the result."""
        tools = self.get_available_tools()
        
        if tool_name not in tools:
            return {"error": f"Tool '{tool_name}' not found"}
        
        try:
            tool_func = tools[tool_name]["function"]
            result = tool_func(**arguments)
            console.print(f"[dim]→ {self.name} used tool:[/dim] [bold]{tool_name}[/bold]")
            return result
        except Exception as e:
            console.print(f"[red]Tool Error ({tool_name}): {e}[/red]")
            return {"error": str(e)}
    
    def think(self, user_message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Main reasoning method - processes input and returns response."""
        # Build messages
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add context if provided
        if context:
            context_str = f"\n\nContext:\n{json.dumps(context, indent=2)}"
            user_message = user_message + context_str
        
        # Add user message
        messages.append({"role": "user", "content": user_message})
        
        # Iterative reasoning loop (with tool calling)
        max_iterations = 5
        for iteration in range(max_iterations):
            response = self.call_llm(messages)
            
            # Try to parse as tool call
            tool_call = self.parse_tool_call(response)
            
            if tool_call:
                tool_name, arguments = tool_call
                
                # Execute tool
                tool_result = self.execute_tool(tool_name, arguments)
                
                # Add to message history
                messages.append({"role": "assistant", "content": response})
                messages.append({
                    "role": "user",
                    "content": f"Tool result: {json.dumps(tool_result, ensure_ascii=False)}"
                })
            else:
                # No tool call - this is the final response
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": response})
                
                # Keep conversation history manageable
                if len(self.conversation_history) > 10:
                    self.conversation_history = self.conversation_history[-10:]
                
                return response
        
        # Max iterations reached
        return "I've reached my reasoning limit. Let me summarize what I found so far..."
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def __repr__(self):
        return f"<{self.__class__.__name__} name='{self.name}' role='{self.role}'>"

