import subprocess
import sys
from pathlib import Path
from typing import Union, Dict, Any  # Import Dict and Any from typing
import os

def is_fastqc_installed() -> bool:
    """
    Checks if FASTQC is installed and accessible in the system's PATH,
    or if it exists in the bio-agent2/FastQC directory.
    Returns True if FASTQC is installed, False otherwise.
    """
    # Check system PATH first
    try:
        subprocess.run(["fastqc", "--version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        pass  # FASTQC not in PATH

    # Check if FASTQC exists in the bio-agent2/FastQC directory
    fastqc_path = Path(__file__).parent.parent / "FastQC" / "fastqc"
    print(f"Checking for FASTQC at: {fastqc_path}")  # Add this line
    executable = os.access(fastqc_path, os.X_OK)
    print(f"os.access(fastqc_path, os.X_OK) returned: {executable}")  # Add this line
    if fastqc_path.is_file() and executable:
        return True

    return False
def display_fastqc_installation_instructions() -> None:
    """
    Prints user-friendly instructions on how to install FASTQC,
    or informs the user that it should be available in the bio-agent2/FastQC directory.
    """
    print("\nFASTQC is not installed in your system's PATH.")
    print("However, it is included in the bio-agent2/FastQC directory.")
    print("Please ensure that this script is run from within the bio-agent2 directory,")
    print("or that the bio-agent2/FastQC directory is in your system's PATH.\n")
    print("If you still encounter issues, you can install FASTQC system-wide following the instructions below:\n")
    print("FASTQC is a standalone Java application. You can download it from:")
    print("https://www.bioinformatics.babraham.ac.uk/projects/fastqc/\n")
    print("Installation instructions for different operating systems:\n")
    print("- macOS (using Homebrew):\n  brew install fastqc\n")
    print("- Debian/Ubuntu (using apt-get):\n  sudo apt-get update && sudo apt-get install fastqc\n")
    print("- Other Linux distributions: Please refer to your distribution's package manager")
    print("  or download the generic Java package from the FASTQC website.\n")
    print("After installation, make sure the 'fastqc' command is accessible in your system's PATH.\n")

def check_fastqc() -> None:
    """
    Checks if FASTQC is installed and displays installation instructions if not found.
    Exits the program if FASTQC is not installed.
    """
    if not is_fastqc_installed():
        display_fastqc_installation_instructions()
        sys.exit(1)

def run_shell_command(command: str, work_dir: Path) -> Dict[str, Any]:
    """
    Executes shell commands and returns the results.
    Prepends the bio-agent2/FastQC directory to the PATH if FASTQC is being called.
    """
    if command.startswith("fastqc"):
        fastqc_path = Path(__file__).parent.parent / "FastQC"
        env = os.environ.copy()
        env["PATH"] = str(fastqc_path) + os.pathsep + env["PATH"]
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                check=True,
                cwd=work_dir,
                env=env
            )
            return {"success": True, "output": result.stdout, "error": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": str(e)}
    else:
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                check=True,
                cwd=work_dir
            )
            return {"success": True, "output": result.stdout, "error": result.stderr}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": str(e)}

import subprocess
import sys
from pathlib import Path
from typing import Union, Dict, Any
import os

def is_fastqc_installed() -> bool:
    """
    Checks if FASTQC is installed and accessible in the system's PATH.
    Returns True if FASTQC is installed, False otherwise.
    """
    try:
        subprocess.run(["fastqc", "--version"], check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False
import ast
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any
from agent.models import ScriptConfig, ExecutionResult

def execute_generated_code(code: str, output_dir: Path) -> Dict[str, Any]:
    try:
        # Let Pydantic handle validation and formatting
        config = ScriptConfig(
            code=code,
            output_dir=output_dir
        )
        
        # Create and execute the formatted script
        temp_file = config.output_dir / "generated_script.py"
        with open(temp_file, "w") as f:
            f.write(config.code)
        
        result = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True,
            check=True
        )
        
        return ExecutionResult(
            status="complete",
            command_executed=config.code,
            output=result.stdout,
            error=result.stderr
        ).model_dump()
        
    except Exception as e:
        return ExecutionResult(
            status="failed",
            command_executed=code,
            error=str(e)
        ).model_dump()

def create_output_directory(input_file: Path) -> Path:
    """
    Creates timestamped output directory based on input filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = input_file.parent / f"bioagent_results_{timestamp}"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir
def run_shell_command(command: str, work_dir: Path) -> Dict[str, Any]:
    """
    Executes shell commands and returns the results
    """
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            check=True,
            cwd=work_dir
        )
        return {"success": True, "output": result.stdout, "error": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": str(e)}

import logging
from datetime import datetime

def setup_logging():
    """Setup logging configuration"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler(f'bioagent_{timestamp}.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('bioagent')
