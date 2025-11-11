"""Coder agent - generates and analyzes code."""
from typing import Dict, Any
from .base_agent import BaseAgent
from tools.code_runner import execute_code
from tools.file_ops import save_file


class CoderAgent(BaseAgent):
    """Agent specialized in code generation and analysis."""
    
    def __init__(self):
        super().__init__(
            name="Coder",
            role="Code Generation and Analysis",
            temperature=0.2
        )
    
    def get_system_prompt(self) -> str:
        return """You are an expert coding agent specialized in software development.

Your capabilities:
- Generate production-quality code
- Explain code and algorithms
- Debug and optimize code
- Write tests and documentation

Available tools:
- execute_code: Run Python code in a sandbox
- save_file: Save code to files

Best practices:
1. Write clean, readable code
2. Include docstrings and comments
3. Follow PEP 8 style (Python)
4. Handle errors gracefully
5. Consider edge cases

Tool call format:
{"tool": "execute_code", "arguments": {"code": "print('hello')", "language": "python"}}

When generating code:
- Explain your approach
- Include usage examples
- Add error handling
- Write tests if requested

Be precise and follow software engineering best practices."""
    
    def get_available_tools(self) -> Dict[str, Any]:
        return {
            "execute_code": {
                "description": "Execute code in a sandbox environment",
                "function": execute_code,
                "parameters": {
                    "code": "string - code to execute",
                    "language": "string - programming language (python, javascript, etc.)",
                    "timeout": "integer - max execution time in seconds"
                }
            },
            "save_file": {
                "description": "Save code to a file",
                "function": save_file,
                "parameters": {
                    "filename": "string - file path",
                    "content": "string - code to save"
                }
            }
        }
    
    def generate_code(self, task: str, language: str = "python", test: bool = False) -> str:
        """Generate code for a specific task."""
        prompt = f"""Generate {language} code for the following task:

Task: {task}

Requirements:
- Clean, production-quality code
- Proper documentation
- Error handling
{'- Include unit tests' if test else ''}

Provide the complete implementation."""
        
        return self.think(prompt)

