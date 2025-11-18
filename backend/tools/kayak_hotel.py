"""Kayak hotel URL generator and scraper."""

from langchain.tools import tool
from loguru import logger
from tools.free_scraper import scrape_website


@tool
def kayak_hotel_url_generator(
    destination: str,
    check_in: str,
    check_out: str,
    adults: int = 1,
    children: int = 0,
    rooms: int = 1,
    sort: str = "recommended"
) -> str:
    """
    Generate Kayak hotel search URL.
    
    Args:
        destination: Destination city or area
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        adults: Number of adults
        children: Number of children
        rooms: Number of rooms
        sort: Sort order (recommended, price, rating, distance)
    
    Returns:
        Kayak search URL
    """
    try:
        logger.info(f"Generating Kayak URL for {destination} from {check_in} to {check_out}")
        
        URL = f"https://www.kayak.com/hotels/{destination}/{check_in}/{check_out}"
        URL += f"/{adults}adults"
        
        if children > 0:
            URL += f"/{children}children"
        
        if rooms > 1:
            URL += f"/{rooms}rooms"
        
        URL += "?currency=USD"
        
        if sort.lower() == "price":
            URL += "&sort=price_a"
        elif sort.lower() == "rating":
            URL += "&sort=userrating_b"
        elif sort.lower() == "distance":
            URL += "&sort=distance_a"
        
        logger.info(f"Generated URL: {URL}")
        return URL
        
    except Exception as e:
        logger.error(f"Error generating Kayak URL: {e}")
        return f"Error: {str(e)}"


@tool
def search_kayak_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    adults: int = 1,
    children: int = 0,
    rooms: int = 1
) -> str:
    """
    Search for hotels on Kayak and return results.
    
    Args:
        destination: Destination city
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)
        adults: Number of adults
        children: Number of children
        rooms: Number of rooms
    
    Returns:
        Scraped hotel information
    """
    try:
        # Generate URL directly
        url = f"https://www.kayak.com/hotels/{destination}/{check_in}/{check_out}"
        url += f"/{adults}adults"
        if children > 0:
            url += f"/{children}children"
        if rooms > 1:
            url += f"/{rooms}rooms"
        url += "?currency=USD&sort=bestflight_a"
        
        if url.startswith("Error"):
            return url
        
        # Scrape the URL
        return scrape_website(url, timeout=45)
        
    except Exception as e:
        logger.error(f"Error searching Kayak hotels: {e}")
        return f"Error searching hotels: {str(e)}"

