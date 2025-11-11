"""Web search tool using DuckDuckGo."""
from typing import List, Dict, Any
from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of search results with title, url, and snippet
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        # Format results
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "url": result.get("href", ""),
                "snippet": result.get("body", ""),
            })
        
        return formatted_results
    
    except Exception as e:
        return [{
            "error": str(e),
            "message": "Failed to perform web search"
        }]


def search_news(query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """
    Search for news articles using DuckDuckGo.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return
    
    Returns:
        List of news results
    """
    try:
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results))
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "snippet": result.get("body", ""),
                "date": result.get("date", ""),
                "source": result.get("source", ""),
            })
        
        return formatted_results
    
    except Exception as e:
        return [{
            "error": str(e),
            "message": "Failed to perform news search"
        }]

