"""State definition for LangGraph travel planning workflow."""

from typing import TypedDict, List, Optional


class TravelPlanState(TypedDict):
    """State that flows through the LangGraph workflow."""
    
    # Input data
    trip_plan_id: str
    travel_request_md: str
    destination: str
    
    # Research & Discovery Agent output
    research_results: Optional[str]  # Combined attractions + restaurants
    
    # Booking & Logistics Agent output
    booking_results: Optional[str]  # Combined flights + hotels
    
    # Planning & Optimization Agent output
    itinerary: Optional[str]
    budget_analysis: Optional[str]
    
    # Final output
    final_response: Optional[str]
    
    # Status tracking
    current_step: str
    errors: List[str]

