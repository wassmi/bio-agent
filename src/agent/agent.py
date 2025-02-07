import subprocess
from pathlib import Path
from typing import Dict, Any
import logging
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from utils.utils import execute_generated_code

class BioAgent:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing BioAgent")
        
        self.llm = ChatGroq(
            temperature=0.1,
            api_key=api_key
        )
        self.logger.debug("LLM initialized")
        
    def execute_command(self, command: str) -> None:
        """Execute a shell command and stream output in real-time"""
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Stream output in real-time
        for line in process.stdout:
            print(line, end='')
            
        process.wait()
    def analyze_file(self, file_path: Path, command: str) -> Dict[str, Any]:
        self.logger.info(f"Starting analysis for {file_path}")
    
        analysis_type = self.llm.predict(
            f"Analyze this task: '{command}' for file {file_path}. "
            f"Answer with only one word: 'script' or 'command'"
        ).strip().lower()
    
        if analysis_type == 'script':
            script = self.llm.predict(
                f"Generate a Python script for: '{command}' for file {file_path}. "
                f"Use exactly this file path: '{file_path}'. "
                f"Return only executable code without comments. "
                f"The script should modify the file content directly."
            )            
            result = execute_generated_code(script, Path.cwd())
            return {
                "status": result["status"],
                "command_executed": result["command_executed"]
            }
        else:
            command_to_run = self.llm.predict(
                f"Generate a command for: '{command}' for file {file_path}. "
                f"Analyze the file type and requirements. Choose appropriate tools. "
                f"Return only the command."
            ).strip()
            self.execute_command(command_to_run)
            return {
                "status": "complete",
                "command_executed": command_to_run
            }            