"""Orchestrator - coordinates multiple agents to accomplish complex tasks."""
import json
from typing import Dict, Any, List
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

from .planner import PlannerAgent
from .researcher import ResearcherAgent
from .analyst import AnalystAgent
from .writer import WriterAgent
from .coder import CoderAgent

console = Console()


class Orchestrator:
    """Coordinates multiple specialized agents to complete complex tasks."""
    
    def __init__(self):
        self.planner = PlannerAgent()
        self.agents = {
            "researcher": ResearcherAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
            "coder": CoderAgent(),
        }
        self.execution_log: List[Dict[str, Any]] = []
    
    def process_task(self, user_query: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Main entry point - process a user task through the agent system."""
        console.print(Panel(
            f"[bold cyan]Processing Task:[/bold cyan]\n{user_query}",
            title="🤖 Orchestrator",
            border_style="cyan"
        ))
        
        # Step 1: Create a plan
        console.print("\n[bold yellow]Step 1: Planning[/bold yellow]")
        plan = self.planner.create_plan(user_query, context)
        
        if "error" in plan:
            console.print(f"[red]Planning failed: {plan.get('error')}[/red]")
            return {
                "status": "error",
                "error": plan.get("error"),
                "logs": self.execution_log
            }
        
        console.print(f"[green]✓[/green] Created plan with {len(plan.get('steps', []))} steps")
        console.print(f"[dim]Rationale: {plan.get('rationale', 'N/A')}[/dim]\n")
        
        # Step 2: Execute the plan
        results = {}
        for step in plan.get("steps", []):
            step_id = step.get("id")
            agent_name = step.get("agent")
            action = step.get("action")
            dependencies = step.get("dependencies", [])
            
            console.print(f"[bold yellow]Step {step_id}:[/bold yellow] {action}")
            console.print(f"[dim]Agent: {agent_name}[/dim]")
            
            # Check dependencies
            for dep_id in dependencies:
                if dep_id not in results:
                    console.print(f"[red]✗ Dependency {dep_id} not satisfied[/red]")
                    results[step_id] = {
                        "status": "failed",
                        "error": f"Dependency {dep_id} not met"
                    }
                    continue
            
            # Get agent
            agent = self.agents.get(agent_name)
            if not agent:
                console.print(f"[red]✗ Unknown agent: {agent_name}[/red]")
                results[step_id] = {
                    "status": "failed",
                    "error": f"Unknown agent: {agent_name}"
                }
                continue
            
            # Prepare context with dependency results
            step_context = context.copy() if context else {}
            for dep_id in dependencies:
                step_context[f"step_{dep_id}_result"] = results.get(dep_id, {}).get("output")
            
            # Execute step
            try:
                output = agent.think(action, step_context)
                results[step_id] = {
                    "status": "success",
                    "output": output,
                    "agent": agent_name
                }
                console.print(f"[green]✓ Completed[/green]\n")
                
                # Log execution
                self.execution_log.append({
                    "step_id": step_id,
                    "agent": agent_name,
                    "action": action,
                    "output": output
                })
                
            except Exception as e:
                console.print(f"[red]✗ Error: {e}[/red]\n")
                results[step_id] = {
                    "status": "error",
                    "error": str(e),
                    "agent": agent_name
                }
        
        # Step 3: Synthesize final result
        console.print("[bold yellow]Step 3: Synthesis[/bold yellow]")
        final_output = self._synthesize_results(user_query, plan, results)
        
        console.print(Panel(
            Markdown(final_output),
            title="✅ Final Result",
            border_style="green"
        ))
        
        return {
            "status": "success",
            "query": user_query,
            "plan": plan,
            "results": results,
            "final_output": final_output,
            "logs": self.execution_log
        }
    
    def _synthesize_results(self, query: str, plan: Dict[str, Any], results: Dict[int, Dict[str, Any]]) -> str:
        """Synthesize results from all steps into a cohesive response."""
        # Collect all outputs
        outputs = []
        for step_id in sorted(results.keys()):
            result = results[step_id]
            if result.get("status") == "success":
                outputs.append(result.get("output", ""))
        
        if not outputs:
            return "I was unable to complete the task successfully. Please check the execution logs for details."
        
        # If only one output, return it
        if len(outputs) == 1:
            return outputs[0]
        
        # Multiple outputs - combine them
        synthesized = f"# Results for: {query}\n\n"
        for i, output in enumerate(outputs, 1):
            step_info = plan.get("steps", [])[i-1] if i-1 < len(plan.get("steps", [])) else {}
            agent_name = step_info.get("agent", "agent")
            synthesized += f"## Step {i}: {agent_name.title()}\n\n"
            synthesized += output + "\n\n"
        
        return synthesized
    
    def get_execution_log(self) -> List[Dict[str, Any]]:
        """Return the execution log."""
        return self.execution_log
    
    def reset(self):
        """Reset all agents and clear execution log."""
        self.planner.reset_conversation()
        for agent in self.agents.values():
            agent.reset_conversation()
        self.execution_log = []

