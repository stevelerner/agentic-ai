"""Data analysis and processing tools."""
from typing import Any, Dict, List, Union
import json


def analyze_data(
    data: Union[Dict, List, str],
    analysis_type: str = "summary"
) -> Dict[str, Any]:
    """
    Analyze structured data.
    
    Args:
        data: Data to analyze (dict, list, or JSON string)
        analysis_type: Type of analysis (summary, trend, comparison)
    
    Returns:
        Dict with analysis results
    """
    try:
        # Parse if string
        if isinstance(data, str):
            data = json.loads(data)
        
        results = {
            "analysis_type": analysis_type,
            "data_type": type(data).__name__,
        }
        
        if isinstance(data, list):
            results["count"] = len(data)
            results["sample"] = data[:3] if len(data) > 3 else data
            
            # Try numeric analysis
            try:
                numeric_data = [float(x) for x in data if isinstance(x, (int, float))]
                if numeric_data:
                    results["numeric_stats"] = {
                        "min": min(numeric_data),
                        "max": max(numeric_data),
                        "mean": sum(numeric_data) / len(numeric_data),
                        "count": len(numeric_data)
                    }
            except:
                pass
        
        elif isinstance(data, dict):
            results["keys"] = list(data.keys())
            results["key_count"] = len(data)
            
            # Sample values
            sample_data = {k: data[k] for k in list(data.keys())[:3]}
            results["sample"] = sample_data
        
        results["status"] = "success"
        return results
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "message": "Failed to analyze data"
        }


def create_summary(content: str, max_length: int = 200) -> Dict[str, str]:
    """
    Create a summary of text content.
    
    Args:
        content: Text to summarize
        max_length: Maximum length in words
    
    Returns:
        Dict with summary
    """
    try:
        words = content.split()
        
        if len(words) <= max_length:
            summary = content
        else:
            # Simple truncation (in production, use proper summarization)
            summary = ' '.join(words[:max_length]) + "..."
        
        return {
            "status": "success",
            "summary": summary,
            "original_length": len(words),
            "summary_length": len(summary.split())
        }
    
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "summary": None
        }


def extract_structured_data(text: str, schema: Dict[str, str]) -> Dict[str, Any]:
    """
    Extract structured data from text based on schema.
    
    Args:
        text: Text to extract from
        schema: Schema describing fields to extract
    
    Returns:
        Dict with extracted data
    """
    # Simple implementation - in production use NLP
    extracted = {}
    
    for field, field_type in schema.items():
        # Basic extraction logic
        if field.lower() in text.lower():
            # Find context around field name
            words = text.split()
            for i, word in enumerate(words):
                if field.lower() in word.lower() and i + 1 < len(words):
                    extracted[field] = words[i + 1]
                    break
    
    return {
        "status": "success",
        "extracted": extracted,
        "fields_found": len(extracted)
    }

