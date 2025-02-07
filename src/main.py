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

def main():
    # Initialize rich console
    console = Console()
    
    with console.status("[bold green]Initializing Bio-Agent...") as status:
        load_dotenv()
        groq_api_key = os.getenv("GROQ_API_KEY")
        
        if not groq_api_key:
            console.print("[bold red]Error:[/] GROQ_API_KEY not found in environment variables")
            return
            
        agent = BioAgent(api_key=groq_api_key)
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--run", help="Command to run")
        parser.add_argument("file", help="Input file path")
        args = parser.parse_args()
        
        file_path = Path(args.file)
        
        # Create analysis panel
        console.print(Panel.fit(
            f"[bold blue]Analysis Request[/]\n"
            f"Command: [green]{args.run}[/]\n"
            f"File: [yellow]{file_path}[/]"
        ))
        
        results = agent.analyze_file(file_path, args.run)
        
        # Print results in a nice table
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Status")
        table.add_column("Command Executed")
        table.add_row(
            results["status"],
            results["command_executed"]
        )
        
        console.print("\n[bold green]Analysis Complete![/]")
        console.print(table)

if __name__ == "__main__":
    main()