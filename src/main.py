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

def display_results(console, results):
    table = Table(title="Analysis Results")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="magenta")
    
    for key, value in results.items():
        table.add_row(str(key), str(value))
    
    console.print(table)

async def chat_loop(agent: BioAgent, console: Console):
    console.print(Panel.fit(
        "[bold blue]Data Science Agent Chat[/]\n"
        "Type 'exit' to quit. You can discuss files naturally!\n"
    ))
    
    while True:
        try:
            user_input = console.input("[bold green]You:[/] ")
            
            if user_input.lower() == 'exit':
                console.print("[bold blue]Goodbye![/]")
                break
            
            # Check for file analysis intent in natural language
            if 'analyze' in user_input.lower() and '.fastq' in user_input.lower():
                # Extract filename using more flexible pattern matching
                file_path = Path(next(word for word in user_input.split() if '.fastq' in word))
                if file_path.exists():
                    results = await agent.analyze_file(file_path, "analyze")
                    display_results(console, results)
                else:
                    console.print(f"[bold red]File not found:[/] {file_path}")
                continue
            
            # Regular chat interaction
            with console.status("[bold green]Thinking..."):
                response = await agent.chat(user_input)
            
            console.print("[bold blue]Assistant:[/] " + response)
            
        except KeyboardInterrupt:
            console.print("\n[bold blue]Goodbye![/]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/] {str(e)}")

async def main():
    console = Console()
    
    parser = argparse.ArgumentParser(
        description="Data Science Agent - Interactive Analysis Assistant"
    )
    parser.add_argument("--file", type=Path, help="Optional file to analyze", required=False)

    args = parser.parse_args()

    # Single status display
    console.print(Panel.fit(        "[bold blue]Data Science Agent Chat[/]\n"
        "Type 'exit' to quit, 'analyze <file>' to analyze a file\n"
    ))
    
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        console.print("[bold red]Error:[/] GROQ_API_KEY not found")
        return
        
    agent = BioAgent(api_key=groq_api_key)
    
    if args.file:
        if not args.file.exists():
            console.print(Panel(f"[bold red]File not found:[/] {args.file}"))
            return
        results = await agent.analyze_file(args.file, "analyze")
        display_results(console, results)
    else:
        await chat_loop(agent, console)

if __name__ == "__main__":
    asyncio.run(main())

def display_results(console, results):
    table = Table(title="Analysis Results")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="magenta")
    
    for key, value in results.items():
        table.add_row(str(key), str(value))
    
    console.print(table)
