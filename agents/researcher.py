"""Research agent - gathers information from the web."""
from typing import Dict, Any
from .base_agent import BaseAgent
from tools.web_search import web_search


class ResearcherAgent(BaseAgent):
    """Agent specialized in information gathering and research."""
    
    def __init__(self):
        super().__init__(
            name="Researcher",
            role="Information Gathering and Research",
            temperature=0.2
        )
    
    def get_system_prompt(self) -> str:
        return """You are a research agent specialized in gathering and synthesizing information.

Your capabilities:
- Search the web for current information
- Evaluate source credibility
- Synthesize findings from multiple sources
- Cite sources properly

When you need to search, respond with:
{"tool": "web_search", "arguments": {"query": "your search query", "max_results": 5}}

After gathering information, provide:
1. Key findings (bullet points)
2. Source citations (with URLs)
3. Relevance assessment
4. Any gaps in available information

Be thorough but concise. Focus on factual, well-sourced information."""
    
    def get_available_tools(self) -> Dict[str, Any]:
        return {
            "web_search": {
                "description": "Search the web using DuckDuckGo",
                "function": web_search,
                "parameters": {
                    "query": "string - search query",
                    "max_results": "integer - number of results (default 5)"
                }
            }
        }
    
    def research(self, topic: str, focus: str = None) -> str:
        """Conduct research on a topic."""
        prompt = f"Research the following topic and provide key findings with sources:\n\nTopic: {topic}"
        if focus:
            prompt += f"\n\nSpecific focus: {focus}"
        
        prompt += "\n\nUse web_search if needed, then synthesize findings."
        
        return self.think(prompt)

