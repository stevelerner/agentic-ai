"""Command-line interface for the agentic AI system."""
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

from agents.orchestrator import Orchestrator

console = Console()


def main():
    """Run the CLI interface."""
    console.print(Panel.fit(
        "[bold cyan]Agentic AI System - CLI[/bold cyan]\n"
        "Multi-Agent Orchestration Demo\n\n"
        "Type your task and press Enter. Type 'quit' or 'exit' to stop.",
        border_style="cyan"
    ))
    
    orchestrator = Orchestrator()
    
    while True:
        try:
            # Get user input
            query = Prompt.ask("\n[bold green]Your task[/bold green]")
            
            if query.lower() in ['quit', 'exit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if not query.strip():
                continue
            
            # Process the task
            console.print()
            result = orchestrator.process_task(query)
            
            # Show summary
            if result.get("status") == "success":
                console.print("\n" + "="*60 + "\n")
                console.print(Panel(
                    result.get("final_output", "No output"),
                    title="✅ Final Result",
                    border_style="green"
                ))
            else:
                console.print(f"\n[red]Error: {result.get('error', 'Unknown error')}[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted. Type 'quit' to exit.[/yellow]")
            continue
        except Exception as e:
            console.print(f"\n[red]Error: {e}[/red]")


if __name__ == "__main__":
    main()

