"""Travel plan service using LangGraph workflow."""

from datetime import datetime, timezone
from models.travel_plan import (
    TravelPlanAgentRequest,
    TravelPlanRequest,
    TravelPlanTeamResponse,
)
from loguru import logger
from agents.langgraph_workflow import run_travel_planning_workflow
import json
import time


def travel_request_to_markdown(data: TravelPlanRequest) -> str:
    """Convert travel plan request to markdown format."""
    travel_vibes = {
        "relaxing": "a peaceful retreat focused on wellness, spa experiences, and leisurely activities",
        "adventure": "thrilling experiences including hiking, water sports, and adrenaline activities",
        "romantic": "intimate experiences with private dining, couples activities, and scenic spots",
        "cultural": "immersive experiences with local traditions, museums, and historical sites",
        "food-focused": "culinary experiences including cooking classes, food tours, and local cuisine",
        "nature": "outdoor experiences with national parks, wildlife, and scenic landscapes",
        "photography": "photogenic locations with scenic viewpoints, cultural sites, and natural wonders",
    }

    travel_styles = {
        "backpacker": "budget-friendly accommodations, local transportation, and authentic experiences",
        "comfort": "mid-range hotels, convenient transportation, and balanced comfort-value ratio",
        "luxury": "premium accommodations, private transfers, and exclusive experiences",
        "eco-conscious": "sustainable accommodations, eco-friendly activities, and responsible tourism",
    }

    pace_levels = {
        0: "1-2 activities per day with plenty of free time and flexibility",
        1: "2-3 activities per day with significant downtime between activities",
        2: "3-4 activities per day with balanced activity and rest periods",
        3: "4-5 activities per day with moderate breaks between activities",
        4: "5-6 activities per day with minimal downtime",
        5: "6+ activities per day with back-to-back scheduling",
    }

    def format_date(date_str: str, is_picker: bool) -> str:
        if not date_str:
            return "Not specified"
        if is_picker:
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                return dt.strftime("%B %d, %Y")
            except ValueError:
                return date_str
        return date_str.strip()

    date_type = data.date_input_type
    is_picker = date_type == "picker"
    start_date = format_date(data.travel_dates.start, is_picker)
    end_date = format_date(data.travel_dates.end, is_picker)
    date_range = (
        f"between {start_date} and {end_date}"
        if end_date and end_date != "Not specified"
        else start_date
    )

    vibes = data.vibes
    vibes_descriptions = [travel_vibes.get(v, v) for v in vibes]

    lines = [
        f"# Travel Plan Request",
        "",
        "## Trip Overview",
        f"- **Traveler:** {data.name.title() if data.name else 'Unnamed Traveler'}",
        f"- **Route:** {data.starting_location.title()} → {data.destination.title()}",
        f"- **Duration:** {data.duration} days ({date_range})",
        "",
        "## Travel Group",
        f"- **Group Size:** {data.adults} adults, {data.children} children",
        f"- **Traveling With:** {data.traveling_with or 'Not specified'}",
        f"- **Age Groups:** {', '.join(data.age_groups) or 'Not specified'}",
        f"- **Rooms Needed:** {data.rooms or 'Not specified'}",
        "",
        "## Budget & Preferences",
        f"- **Budget per person:** {data.budget} {data.budget_currency} ({'Flexible' if data.budget_flexible else 'Fixed'})",
        f"- **Travel Style:** {travel_styles.get(data.travel_style, data.travel_style or 'Not specified')}",
        f"- **Preferred Pace:** {', '.join([pace_levels.get(p, str(p)) for p in data.pace]) or 'Not specified'}",
        "",
        "## Trip Preferences",
    ]

    if vibes_descriptions:
        lines.append("- **Travel Vibes:**")
        for vibe in vibes_descriptions:
            lines.append(f"  - {vibe}")
    else:
        lines.append("- **Travel Vibes:** Not specified")

    if data.priorities:
        lines.append(f"- **Top Priorities:** {', '.join(data.priorities)}")
    if data.interests:
        lines.append(f"- **Interests:** {data.interests}")

    lines.extend([
        "",
        "## Destination Context",
        f"- **Previous Visit:** {data.been_there_before.capitalize() if data.been_there_before else 'Not specified'}",
        f"- **Loved Places:** {data.loved_places or 'Not specified'}",
        f"- **Additional Notes:** {data.additional_info or 'Not specified'}",
    ])

    return "\n".join(lines)


async def generate_travel_plan(request: TravelPlanAgentRequest) -> str:
    """
    Generate a travel plan using LangGraph workflow.
    
    Args:
        request: Travel plan request with trip_plan_id and travel_plan data
    
    Returns:
        JSON string with complete travel plan
    """
    trip_plan_id = request.trip_plan_id
    logger.info(f"Generating travel plan for tripPlanId: {trip_plan_id}")

    time_start = time.time()

    try:
        # Convert request to markdown
        travel_request_md = travel_request_to_markdown(request.travel_plan)
        logger.info(f"Travel request markdown prepared")

        # Run LangGraph workflow
        logger.info("Starting LangGraph workflow")
        result = await run_travel_planning_workflow(
            trip_plan_id=trip_plan_id,
            travel_request_md=travel_request_md,
            destination=request.travel_plan.destination
        )

        time_end = time.time()
        logger.info(f"Total time taken: {time_end - time_start:.2f} seconds")

        # Compile final response in the expected format
        final_response = json.dumps({
            "itinerary": {
                "research_results": result.get("research_results"),
                "booking_results": result.get("booking_results"),
                "itinerary": result.get("itinerary"),
                "budget_analysis": result.get("budget_analysis"),
            },
            "research_agent_response": result.get("research_results"),
            "booking_agent_response": result.get("booking_results"),
            "itinerary_agent_response": result.get("itinerary"),
            "budget_agent_response": result.get("budget_analysis"),
            "current_step": result.get("current_step"),
            "errors": result.get("errors", []),
            "trip_plan_id": trip_plan_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, indent=2)

        logger.info(f"Travel plan generated successfully for {trip_plan_id}")
        return final_response

    except Exception as e:
        logger.error(
            f"Error generating travel plan for {trip_plan_id}: {str(e)}", exc_info=True
        )
        # Return error response
        error_response = json.dumps({
            "success": False,
            "error": str(e),
            "trip_plan_id": trip_plan_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, indent=2)
        return error_response

