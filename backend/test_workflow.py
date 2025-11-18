"""Test script for LangGraph workflow."""

import asyncio
from models.travel_plan import TravelPlanRequest, TravelPlanAgentRequest
from services.plan_service import generate_travel_plan
from loguru import logger


async def test_workflow():
    """Test the complete travel planning workflow."""
    
    # Create a test travel plan request
    travel_plan = TravelPlanRequest(
        name="Test User",
        destination="Paris",
        starting_location="New York",
        duration=5,
        adults=2,
        children=0,
        budget=5000,
        budget_currency="USD",
        travel_style="comfort",
        vibes=["romantic", "cultural"],
        priorities=["museums", "food"],
        interests="Art, history, French cuisine",
    )
    
    request = TravelPlanAgentRequest(
        trip_plan_id="test-trip-001",
        travel_plan=travel_plan
    )
    
    logger.info("Starting test workflow...")
    logger.info(f"Destination: {travel_plan.destination}")
    logger.info(f"Duration: {travel_plan.duration} days")
    
    try:
        result = await generate_travel_plan(request)
        logger.info("Workflow completed successfully!")
        logger.info(f"Result length: {len(result)} characters")
        print("\n" + "="*80)
        print("RESULT:")
        print("="*80)
        print(result[:2000] + "..." if len(result) > 2000 else result)
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_workflow())

