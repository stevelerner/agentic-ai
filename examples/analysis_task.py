"""Example: Data analysis task."""
import sys
sys.path.insert(0, '/app')

from rich.console import Console
from agents.orchestrator import Orchestrator

console = Console()


def main():
    """Run an analysis task example."""
    console.print("\n[bold cyan]Example: Analysis Task[/bold cyan]\n")
    
    orchestrator = Orchestrator()
    
    task = """Analyze the pros and cons of different database architectures for a high-traffic web application:
    
    Compare:
    - Relational databases (PostgreSQL, MySQL)
    - NoSQL databases (MongoDB, Cassandra)
    - NewSQL databases (CockroachDB)
    - Cache layers (Redis, Memcached)
    
    Consider:
    - Performance and scalability
    - Consistency guarantees
    - Operational complexity
    - Cost
    
    Provide recommendations for different use cases."""
    
    console.print(f"[bold]Task:[/bold] {task}\n")
    
    result = orchestrator.process_task(task)
    
    if result.get("status") == "success":
        console.print("\n[green]✓ Analysis completed![/green]")
    else:
        console.print(f"\n[red]✗ Analysis failed: {result.get('error')}[/red]")


if __name__ == "__main__":
    main()

