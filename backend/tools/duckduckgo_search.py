"""DuckDuckGo search tool (free, no API key required)."""

from langchain.tools import tool
try:
    from ddgs import DDGS  # New package name
except ImportError:
    from duckduckgo_search import DDGS  # Fallback to old name
from loguru import logger
from typing import Optional


@tool
def duckduckgo_search(query: str, max_results: int = 10) -> str:
    """
    Search the web using DuckDuckGo (free, no API key required).
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 10)
    
    Returns:
        Formatted string with search results
    """
    try:
        logger.info(f"DuckDuckGo search: {query}")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            return f"No results found for: {query}"
        
        formatted_results = []
        for i, result in enumerate(results[:max_results], 1):
            formatted_results.append(
                f"{i}. {result.get('title', 'No title')}\n"
                f"   URL: {result.get('href', 'No URL')}\n"
                f"   {result.get('body', 'No description')}\n"
            )
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error in DuckDuckGo search: {e}")
        return f"Error searching: {str(e)}"


@tool
def duckduckgo_destination_search(destination: str, query_type: str = "attractions") -> str:
    """
    Search for destination information (attractions, restaurants, etc.).
    
    Args:
        destination: Destination name
        query_type: Type of search (attractions, restaurants, hotels, etc.)
    
    Returns:
        Formatted search results
    """
    query_map = {
        "attractions": f"{destination} tourist attractions landmarks",
        "restaurants": f"{destination} best restaurants dining",
        "hotels": f"{destination} hotels accommodations",
        "activities": f"{destination} things to do activities",
    }
    
    search_query = query_map.get(query_type, f"{destination} {query_type}")
    
    # Call the underlying function directly to avoid tool-to-tool calling issues
    try:
        logger.info(f"DuckDuckGo destination search: {destination} ({query_type})")
        
        with DDGS() as ddgs:
            results = list(ddgs.text(search_query, max_results=10))
        
        if not results:
            return f"No results found for: {search_query}"
        
        formatted_results = []
        for i, result in enumerate(results[:10], 1):
            formatted_results.append(
                f"{i}. {result.get('title', 'No title')}\n"
                f"   URL: {result.get('href', 'No URL')}\n"
                f"   {result.get('body', 'No description')}\n"
            )
        
        return "\n".join(formatted_results)
        
    except Exception as e:
        logger.error(f"Error in DuckDuckGo destination search: {e}")
        return f"Error searching: {str(e)}"

