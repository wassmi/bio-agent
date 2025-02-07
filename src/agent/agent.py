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
    async def analyze_file(self, file_path: Path, command: str) -> Dict[str, Any]:
        self.logger.info(f"Starting analysis for {file_path}")
    
        analysis_type = self.llm.invoke(
            f"Analyze this task: '{command}' for file {file_path}. "
            f"Answer with only one word: 'script' or 'command'"
        ).content.strip().lower()
    
        if analysis_type == 'script':
            script = self.llm.invoke(
                f"Generate a Python script for: '{command}' for file {file_path}. "
                f"Return only the executable Python code, no markdown, no explanations."
            ).content
            
            result = execute_generated_code(script, Path.cwd())
            return {
                "status": result["status"],
                "command_executed": result["command_executed"]
            }
        else:
            command_to_run = self.llm.invoke(
                f"Generate a single shell command for: '{command}' for file {file_path}. "
                f"Return only the command itself, no explanations or markdown formatting."
            ).content.strip()
            
            # Initialize default result structure
            result = {
                "status": "complete",
                "command_executed": command_to_run,
                "output": "",
                "error": ""
            }
            
            # Execute command and update result if successful
            execution_result = self.execute_command(command_to_run)
            if execution_result:
                result.update(execution_result)
                
            return result                        