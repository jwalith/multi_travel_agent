"""Free web scraping tool using BeautifulSoup and requests."""

from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from loguru import logger
from typing import Optional
import time


@tool
def scrape_website(url: str, timeout: int = 30) -> str:
    """
    Scrape a website and return text content (free, using BeautifulSoup).
    
    Args:
        url: URL to scrape
        timeout: Request timeout in seconds (default: 30)
    
    Returns:
        Extracted text content from the webpage
    """
    try:
        logger.info(f"Scraping URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Get text
        text = soup.get_text()
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Limit to first 5000 characters to avoid token limits
        if len(text) > 5000:
            text = text[:5000] + "... [truncated]"
        
        logger.info(f"Successfully scraped {len(text)} characters from {url}")
        return text
        
    except requests.exceptions.Timeout:
        logger.error(f"Timeout scraping {url}")
        return f"Timeout error: Could not scrape {url} within {timeout} seconds"
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error scraping {url}: {e}")
        return f"Error scraping {url}: {str(e)}"
    
    except Exception as e:
        logger.error(f"Unexpected error scraping {url}: {e}")
        return f"Unexpected error: {str(e)}"


@tool
def scrape_kayak_hotel(url: str) -> str:
    """
    Scrape Kayak hotel search results.
    
    Args:
        url: Kayak hotel search URL
    
    Returns:
        Extracted hotel information
    """
    return scrape_website(url, timeout=45)

