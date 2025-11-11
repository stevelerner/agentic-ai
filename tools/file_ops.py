"""File operation tools for agents."""
import os
from pathlib import Path
from typing import Union


# Base directory for file operations (can be mounted volume in Docker)
BASE_DIR = Path(os.getenv("OUTPUT_DIR", "/app/outputs"))
BASE_DIR.mkdir(parents=True, exist_ok=True)


def save_file(filename: str, content: str) -> Dict[str, str]:
    """
    Save content to a file.
    
    Args:
        filename: Name or path of the file
        content: Content to save
    
    Returns:
        Dict with status and file path
    """
    try:
        # Ensure filename is relative to BASE_DIR
        file_path = BASE_DIR / filename
        
        # Create parent directories if needed
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "status": "success",
            "path": str(file_path),
            "message": f"Saved to {file_path}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": f"Failed to save file: {e}"
        }


def read_file(filename: str) -> Dict[str, Union[str, None]]:
    """
    Read content from a file.
    
    Args:
        filename: Name or path of the file
    
    Returns:
        Dict with status and content
    """
    try:
        file_path = BASE_DIR / filename
        
        if not file_path.exists():
            return {
                "status": "error",
                "content": None,
                "message": f"File not found: {filename}"
            }
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "status": "success",
            "content": content,
            "message": f"Read {len(content)} characters from {filename}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "content": None,
            "error": str(e),
            "message": f"Failed to read file: {e}"
        }


def list_files(directory: str = ".") -> Dict[str, Any]:
    """
    List files in a directory.
    
    Args:
        directory: Directory path (relative to BASE_DIR)
    
    Returns:
        Dict with status and list of files
    """
    try:
        dir_path = BASE_DIR / directory
        
        if not dir_path.exists():
            return {
                "status": "error",
                "files": [],
                "message": f"Directory not found: {directory}"
            }
        
        files = []
        for item in dir_path.iterdir():
            files.append({
                "name": item.name,
                "type": "directory" if item.is_dir() else "file",
                "size": item.stat().st_size if item.is_file() else None
            })
        
        return {
            "status": "success",
            "files": files,
            "message": f"Found {len(files)} items"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "files": [],
            "error": str(e),
            "message": f"Failed to list files: {e}"
        }


# Fix the type hint import
from typing import Any, Dict

