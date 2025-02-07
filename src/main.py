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

def main():
    console = Console()
    
    parser = argparse.ArgumentParser(
        description="BioAgent - Bioinformatics Workflow Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--run", 
        help="Command to run",
        required=True
    )
    parser.add_argument(
        "file", 
        help="Input file path (e.g., sample.fastq)",
        type=str
    )

    try:
        args = parser.parse_args()
    except SystemExit:
        console.print(Panel(
            "[bold yellow]Missing Input File[/]\n\n"
            "[bold white]Your command needs an input file to work on.[/]\n\n"
            "[bold green]Correct Format:[/]\n"
            "python src/main.py --run \"your command\" input_file.fastq\n\n"
            "[bold green]Example:[/]\n"
            "python src/main.py --run \"analyze this file\" SRR11140744_R1.fastq",
            title="🔍 Usage Guide",
            border_style="yellow"
        ))
        return

    try:
        with console.status("[bold green]Initializing Bio-Agent...") as status:
            load_dotenv()
            groq_api_key = os.getenv("GROQ_API_KEY")
            
            if not groq_api_key:
                console.print("[bold red]Error:[/] GROQ_API_KEY not found in environment variables")
                return
                
            agent = BioAgent(api_key=groq_api_key)
            
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
        
    except Exception as e:
        console.print(Panel(
            "[bold red]Error:[/] Please provide both the command and input file\n\n"
            "[bold green]Example usage:[/]\n"
            "python src/main.py --run \"analyze this file\" input.fastq",
            title="Usage Guide"
        ))
        return

if __name__ == "__main__":
    main()   