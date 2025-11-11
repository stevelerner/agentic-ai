"""Analyst agent - processes and analyzes data."""
from typing import Dict, Any
from .base_agent import BaseAgent
from tools.data_tools import analyze_data, create_summary


class AnalystAgent(BaseAgent):
    """Agent specialized in data analysis and synthesis."""
    
    def __init__(self):
        super().__init__(
            name="Analyst",
            role="Data Analysis and Synthesis",
            temperature=0.2
        )
    
    def get_system_prompt(self) -> str:
        return """You are an analytical agent specialized in processing and interpreting information.

Your capabilities:
- Identify patterns and trends in data
- Synthesize information from multiple sources
- Draw insights and conclusions
- Provide evidence-based recommendations

Available tools:
- analyze_data: Process structured data and extract insights
- create_summary: Generate concise summaries

When analyzing, focus on:
1. Key patterns and trends
2. Notable outliers or anomalies
3. Correlations and relationships
4. Actionable insights
5. Confidence levels in findings

Tool call format:
{"tool": "analyze_data", "arguments": {"data": {...}, "analysis_type": "trend"}}

Be objective and evidence-based. Clearly distinguish between facts and interpretations."""
    
    def get_available_tools(self) -> Dict[str, Any]:
        return {
            "analyze_data": {
                "description": "Analyze structured data",
                "function": analyze_data,
                "parameters": {
                    "data": "dict or list - data to analyze",
                    "analysis_type": "string - type of analysis (trend, summary, comparison)"
                }
            },
            "create_summary": {
                "description": "Create a concise summary of information",
                "function": create_summary,
                "parameters": {
                    "content": "string - content to summarize",
                    "max_length": "integer - max words in summary"
                }
            }
        }
    
    def analyze(self, data: Any, analysis_type: str = "general") -> str:
        """Analyze data and provide insights."""
        prompt = f"""Analyze the following data and provide insights:

Data: {data}

Analysis focus: {analysis_type}

Provide:
1. Key findings
2. Trends or patterns
3. Recommendations
4. Confidence level"""
        
        return self.think(prompt)

