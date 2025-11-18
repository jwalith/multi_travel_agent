"""Wikipedia API tool (free, no API key required)."""

from langchain.tools import tool
import wikipedia
from loguru import logger
from typing import Optional


@tool
def wikipedia_search(query: str, sentences: int = 5) -> str:
    """
    Search Wikipedia for information (free, no API key required).
    
    Args:
        query: Search query string
        sentences: Number of sentences to return from summary (default: 5)
    
    Returns:
        Wikipedia article summary
    """
    try:
        logger.info(f"Wikipedia search: {query}")
        
        # Search for pages
        search_results = wikipedia.search(query, results=1)
        
        if not search_results:
            return f"No Wikipedia article found for: {query}"
        
        # Get page summary
        page = wikipedia.page(search_results[0])
        summary = wikipedia.summary(search_results[0], sentences=sentences)
        
        return f"Title: {page.title}\n\n{summary}\n\nURL: {page.url}"
        
    except wikipedia.exceptions.DisambiguationError as e:
        # If disambiguation, use first option
        try:
            page = wikipedia.page(e.options[0])
            summary = wikipedia.summary(e.options[0], sentences=sentences)
            return f"Title: {page.title}\n\n{summary}\n\nURL: {page.url}"
        except Exception as e2:
            logger.error(f"Error in Wikipedia disambiguation: {e2}")
            return f"Multiple options found for {query}. Please be more specific."
    
    except Exception as e:
        logger.error(f"Error in Wikipedia search: {e}")
        return f"Error searching Wikipedia: {str(e)}"


@tool
def wikipedia_destination_info(destination: str) -> str:
    """
    Get comprehensive information about a destination from Wikipedia.
    
    Args:
        destination: Destination name (city, country, landmark, etc.)
    
    Returns:
        Wikipedia information about the destination
    """
    # Call the underlying function directly to avoid tool-to-tool calling issues
    try:
        logger.info(f"Wikipedia destination search: {destination}")
        
        # Search for pages
        search_results = wikipedia.search(f"{destination} travel tourism", results=1)
        
        if not search_results:
            return f"No Wikipedia article found for: {destination}"
        
        # Get page summary
        page = wikipedia.page(search_results[0])
        summary = wikipedia.summary(search_results[0], sentences=10)
        
        return f"Title: {page.title}\n\n{summary}\n\nURL: {page.url}"
        
    except wikipedia.exceptions.DisambiguationError as e:
        # If disambiguation, use first option
        try:
            page = wikipedia.page(e.options[0])
            summary = wikipedia.summary(e.options[0], sentences=10)
            return f"Title: {page.title}\n\n{summary}\n\nURL: {page.url}"
        except Exception as e2:
            logger.error(f"Error in Wikipedia disambiguation: {e2}")
            return f"Multiple options found for {destination}. Please be more specific."
    
    except Exception as e:
        logger.error(f"Error in Wikipedia destination search: {e}")
        return f"Error searching Wikipedia: {str(e)}"

