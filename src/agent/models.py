from pydantic import BaseModel, field_validator
from typing import Optional
from pathlib import Path
import ast
import black

class ScriptConfig(BaseModel):
    code: str
    output_dir: Path
    
    @field_validator('code')
    def format_python_code(cls, code: str) -> str:
        # Validate it's valid Python
        ast.parse(code)
        # Format using black
        return black.format_str(code, mode=black.FileMode())

class ExecutionResult(BaseModel):
    status: str
    command_executed: str
    output: Optional[str] = None
    error: Optional[str] = None
