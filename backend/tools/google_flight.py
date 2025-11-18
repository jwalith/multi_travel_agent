"""Google Flights search tool using fast-flights library."""

from langchain.tools import tool
from fast_flights import FlightData, Passengers, Result, get_flights
from typing import Literal
from loguru import logger


@tool
def get_google_flights(
    departure: str,
    destination: str,
    date: str,
    trip: Literal["one-way", "round-trip"] = "one-way",
    adults: int = 1,
    children: int = 0,
    cabin_class: Literal["first", "business", "premium-economy", "economy"] = "economy",
) -> str:
    """
    Get flights from Google Flights using fast-flights library.
    
    Args:
        departure: Departure airport code (e.g., "BOM", "DEL")
        destination: Destination airport code
        date: Flight date in YYYY-MM-DD format
        trip: Trip type (one-way or round-trip)
        adults: Number of adults
        children: Number of children
        cabin_class: Cabin class preference
    
    Returns:
        Formatted string with flight options
    """
    try:
        logger.info(f"Searching flights: {departure} -> {destination} on {date}")
        
        result: Result = get_flights(
            flight_data=[
                FlightData(date=date, from_airport=departure, to_airport=destination)
            ],
            trip=trip,
            seat=cabin_class,
            passengers=Passengers(
                adults=adults, children=children, infants_in_seat=0, infants_on_lap=0
            ),
            fetch_mode="fallback",
        )
        
        if not result.flights:
            return f"No flights found for {departure} to {destination} on {date}"
        
        formatted_flights = []
        for i, flight in enumerate(result.flights[:5], 1):  # Top 5 flights
            flight_info = f"{i}. {flight.get('airline', 'Unknown')} - {flight.get('flight_number', 'N/A')}\n"
            flight_info += f"   Departure: {flight.get('departure_time', 'N/A')}\n"
            flight_info += f"   Arrival: {flight.get('arrival_time', 'N/A')}\n"
            flight_info += f"   Duration: {flight.get('duration', 'N/A')}\n"
            flight_info += f"   Price: {flight.get('price', 'N/A')}\n"
            flight_info += f"   Stops: {flight.get('stops', 0)}\n"
            formatted_flights.append(flight_info)
        
        return "\n".join(formatted_flights)
        
    except Exception as e:
        logger.error(f"Error getting flights: {e}")
        return f"Error searching flights: {str(e)}"

