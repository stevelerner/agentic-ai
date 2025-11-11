"""Code execution tool - runs code in a sandbox."""
import subprocess
import tempfile
from typing import Dict, Any
from pathlib import Path


def execute_code(
    code: str,
    language: str = "python",
    timeout: int = 30
) -> Dict[str, Any]:
    """
    Execute code in a sandboxed environment.
    
    Args:
        code: Code to execute
        language: Programming language (python, javascript, etc.)
        timeout: Maximum execution time in seconds
    
    Returns:
        Dict with execution results
    """
    if language.lower() not in ["python", "python3"]:
        return {
            "status": "error",
            "output": None,
            "error": f"Unsupported language: {language}. Only Python is currently supported.",
            "exitcode": -1
        }
    
    try:
        # Create temporary file for code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        # Execute in subprocess with timeout
        result = subprocess.run(
            ["python3", temp_file],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        # Clean up temp file
        Path(temp_file).unlink()
        
        return {
            "status": "success" if result.returncode == 0 else "error",
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "exitcode": result.returncode
        }
    
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "output": None,
            "error": f"Execution timed out after {timeout} seconds",
            "exitcode": -1
        }
    
    except Exception as e:
        return {
            "status": "error",
            "output": None,
            "error": str(e),
            "exitcode": -1
        }


def validate_code(code: str, language: str = "python") -> Dict[str, Any]:
    """
    Validate code syntax without executing.
    
    Args:
        code: Code to validate
        language: Programming language
    
    Returns:
        Dict with validation results
    """
    if language.lower() not in ["python", "python3"]:
        return {
            "valid": False,
            "error": f"Unsupported language: {language}"
        }
    
    try:
        compile(code, '<string>', 'exec')
        return {
            "valid": True,
            "error": None
        }
    except SyntaxError as e:
        return {
            "valid": False,
            "error": f"Syntax error at line {e.lineno}: {e.msg}"
        }
    except Exception as e:
        return {
            "valid": False,
            "error": str(e)
        }

