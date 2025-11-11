"""Example: Research task with multi-agent collaboration."""
import sys
sys.path.insert(0, '/app')

from rich.console import Console
from agents.orchestrator import Orchestrator

console = Console()


def main():
    """Run a research task example."""
    console.print("\n[bold cyan]Example: Research Task[/bold cyan]\n")
    
    orchestrator = Orchestrator()
    
    task = """Research the latest developments in AI agents and agentic AI systems.
    
    Focus on:
    1. Key concepts and terminology
    2. Recent breakthroughs (2023-2024)
    3. Practical applications
    4. Future trends
    
    Create a comprehensive report with sources."""
    
    console.print(f"[bold]Task:[/bold] {task}\n")
    
    result = orchestrator.process_task(task)
    
    if result.get("status") == "success":
        console.print("\n[green]✓ Task completed successfully![/green]")
        console.print(f"\nSteps executed: {len(result.get('results', {}))}")
        console.print(f"Final output length: {len(result.get('final_output', ''))} characters")
    else:
        console.print(f"\n[red]✗ Task failed: {result.get('error')}[/red]")


if __name__ == "__main__":
    main()

