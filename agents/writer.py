"""Writer agent - creates documents and reports."""
from typing import Dict, Any
from .base_agent import BaseAgent
from tools.file_ops import save_file, read_file


class WriterAgent(BaseAgent):
    """Agent specialized in content creation and documentation."""
    
    def __init__(self):
        super().__init__(
            name="Writer",
            role="Content Creation and Documentation",
            temperature=0.4  # Slightly higher for creativity
        )
    
    def get_system_prompt(self) -> str:
        return """You are a professional writer agent specialized in creating clear, engaging content.

Your capabilities:
- Write reports, documentation, and articles
- Structure information logically
- Adapt tone and style to audience
- Create well-formatted markdown documents

Available tools:
- save_file: Save content to a file
- read_file: Read existing files

When writing, ensure:
1. Clear structure (intro, body, conclusion)
2. Proper formatting (headers, lists, emphasis)
3. Citations for sources
4. Professional tone
5. Correct grammar and spelling

Tool call format:
{"tool": "save_file", "arguments": {"filename": "report.md", "content": "# Report..."}}

Focus on clarity, accuracy, and readability."""
    
    def get_available_tools(self) -> Dict[str, Any]:
        return {
            "save_file": {
                "description": "Save content to a file",
                "function": save_file,
                "parameters": {
                    "filename": "string - file path",
                    "content": "string - content to save"
                }
            },
            "read_file": {
                "description": "Read content from a file",
                "function": read_file,
                "parameters": {
                    "filename": "string - file path"
                }
            }
        }
    
    def write(self, content_type: str, topic: str, context: Dict[str, Any] = None) -> str:
        """Write content of specified type."""
        prompt = f"""Create a {content_type} about: {topic}

Requirements:
- Professional quality
- Well-structured
- Properly formatted markdown
- Include relevant sections

If you want to save the output, use the save_file tool."""
        
        return self.think(prompt, context)

