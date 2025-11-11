"""Example: Code generation task."""
import sys
sys.path.insert(0, '/app')

from rich.console import Console
from agents.orchestrator import Orchestrator

console = Console()


def main():
    """Run a coding task example."""
    console.print("\n[bold cyan]Example: Coding Task[/bold cyan]\n")
    
    orchestrator = Orchestrator()
    
    task = """Generate a production-ready Python REST API with the following features:
    
    1. User authentication (JWT tokens)
    2. CRUD operations for a 'tasks' resource
    3. Input validation
    4. Error handling
    5. Basic unit tests
    6. API documentation
    
    Use FastAPI framework and include:
    - Main application file
    - Authentication module
    - Data models
    - API routes
    - Tests
    - README with setup instructions"""
    
    console.print(f"[bold]Task:[/bold] {task}\n")
    
    result = orchestrator.process_task(task)
    
    if result.get("status") == "success":
        console.print("\n[green]✓ Code generation completed![/green]")
        console.print("\nCheck /app/outputs for generated files.")
    else:
        console.print(f"\n[red]✗ Code generation failed: {result.get('error')}[/red]")


if __name__ == "__main__":
    main()

