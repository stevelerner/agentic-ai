"""Planning agent - creates execution plans for complex tasks."""
from typing import Dict, Any
from .base_agent import BaseAgent


class PlannerAgent(BaseAgent):
    """Agent specialized in breaking down complex tasks into executable steps."""
    
    def __init__(self):
        super().__init__(
            name="Planner",
            role="Task Planning and Decomposition",
            temperature=0.3
        )
    
    def get_system_prompt(self) -> str:
        return """You are a strategic planning agent. Your role is to:

1. Analyze user requests and break them into clear, actionable steps
2. Identify which specialist agents are needed (Researcher, Analyst, Writer, Coder)
3. Determine dependencies between steps
4. Create a structured execution plan

When creating a plan, respond with a JSON object:
{
    "steps": [
        {
            "id": 1,
            "agent": "researcher",
            "action": "Search for recent AI agent research papers",
            "dependencies": [],
            "expected_output": "List of relevant papers with summaries"
        },
        {
            "id": 2,
            "agent": "analyst",
            "action": "Identify key trends from research",
            "dependencies": [1],
            "expected_output": "Summary of 3-5 major trends"
        }
    ],
    "rationale": "Why this plan makes sense"
}

Available agents:
- researcher: Web search, information gathering
- analyst: Data analysis, trend identification, synthesis
- writer: Content creation, documentation, reports
- coder: Code generation, technical implementation

Be concise but thorough. Focus on actionable steps."""
    
    def get_available_tools(self) -> Dict[str, Any]:
        """Planner doesn't need tools - it creates plans."""
        return {}
    
    def create_plan(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create an execution plan for a task."""
        prompt = f"""Create a detailed execution plan for this task:

Task: {task}

Consider:
- What information needs to be gathered?
- What analysis is required?
- What output format is expected?
- Which agents are best suited for each step?

Respond ONLY with the JSON plan structure."""
        
        response = self.think(prompt, context)
        
        # Try to parse the plan
        import json
        try:
            # Find JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                plan_json = response[start:end]
                plan = json.loads(plan_json)
                return plan
        except Exception as e:
            # Fallback to simple plan
            return {
                "steps": [
                    {
                        "id": 1,
                        "agent": "researcher",
                        "action": task,
                        "dependencies": [],
                        "expected_output": "Results"
                    }
                ],
                "rationale": f"Fallback plan due to parsing error: {e}"
            }
        
        return {
            "steps": [],
            "rationale": "Could not create plan",
            "error": "Failed to parse plan from response"
        }

