import subprocess
import sys
from pathlib import Path
from typing import Union

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

def display_fastqc_installation_instructions() -> None:
    """
    Prints user-friendly instructions on how to install FASTQC.
    """
    print("\nFASTQC is not installed. Please install it following the instructions below:\n")
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

def validate_fastq_file(file_path: Union[str, Path]) -> bool:
    """
    Validates if the given file is a FASTQ file.
    Returns True if valid, False otherwise.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return False
    
    # Check file extension
    valid_extensions = {'.fastq', '.fq', '.fastq.gz', '.fq.gz'}
    if not any(str(file_path).lower().endswith(ext) for ext in valid_extensions):
        return False
    
    return True

import subprocess
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

def execute_generated_code(code: str, output_dir: Path) -> Dict[str, Any]:
    import os
    import sys
    import subprocess

    try:
        # Create a temporary Python file
        temp_file = output_dir / "generated_script.py"
        with open(temp_file, "w") as f:
            f.write(code)
        
        # Execute the script with the output directory as an environment variable
        env = os.environ.copy()
        env["OUTPUT_DIR"] = str(output_dir)
        result = subprocess.run(
            [sys.executable, str(temp_file)],
            capture_output=True,
            text=True,
            env=env
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

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
