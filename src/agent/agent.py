import subprocess
from pathlib import Path
from typing import Dict, Any
import logging
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

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
    
        # Get command from LLM
        response = self.llm.predict(f"Generate the command to {command} for file {file_path}. Return only the command, no explanations.")
    
        # Extract command from response
        command_to_run = response.strip()
    
        # Execute the command
        self.execute_command(command_to_run)
    
        return {
            "status": "complete",
            "command_executed": command_to_run
        }