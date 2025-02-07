from dotenv import load_dotenv
import os
from pathlib import Path
from agent.agent import BioAgent
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.live import Live
from rich.table import Table
import argparse
import sys
import asyncio

async def main():
    console = Console()
    
    parser = argparse.ArgumentParser(
        description="BioAgent - Bioinformatics Workflow Assistant"
    )
    parser.add_argument("--run", required=True)
    parser.add_argument("file", type=Path)

    args = parser.parse_args()
    file_path = args.file

    # Validate file existence
    if not file_path.exists():
        console.print(Panel(
            f"[bold red]File not found:[/] {file_path}\n\n"
            "[bold green]Please check:[/]\n"
            "1. The file path is correct\n"
            "2. The file exists in the specified location\n"
            "3. You have read permissions for the file",
            title="🔍 File Check"
        ))
        return

    with console.status("[bold green]Initializing Bio-Agent...") as status:
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not groq_api_key:
            console.print("[bold red]Error:[/] GROQ_API_KEY not found")
            return
            
        agent = BioAgent(api_key=groq_api_key)
        
        console.print(Panel.fit(
            f"[bold blue]Analysis Request[/]\n"
            f"Command: [green]{args.run}[/]\n"
            f"File: [yellow]{file_path}[/]"
        ))
        
        results = await agent.analyze_file(file_path, args.run)
        
        console.print("\n[bold green]Analysis Complete![/]")
        
        # Define the display_results function
        def display_results(console, results):
            table = Table(title="Analysis Results")
            table.add_column("Key", style="cyan")
            table.add_column("Value", style="magenta")
            
            for key, value in results.items():
                table.add_row(str(key), str(value))
            
            console.print(table)
        
        display_results(console, results)

if __name__ == "__main__":
    asyncio.run(main())
