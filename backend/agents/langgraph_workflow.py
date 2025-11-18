"""LangGraph workflow for travel planning."""

from langgraph.graph import StateGraph, END
from agents.langgraph_state import TravelPlanState
from agents.langgraph_nodes import (
    research_discovery_node,
    booking_logistics_node,
    planning_optimization_node
)
from loguru import logger


def create_travel_planning_graph():
    """Create the LangGraph workflow for travel planning."""
    
    logger.info("Creating LangGraph workflow")
    
    # Create the graph
    workflow = StateGraph(TravelPlanState)
    
    # Add nodes (each agent becomes a node)
    workflow.add_node("research_discovery", research_discovery_node)
    workflow.add_node("booking_logistics", booking_logistics_node)
    workflow.add_node("planning_optimization", planning_optimization_node)
    
    # Define the sequential flow
    workflow.set_entry_point("research_discovery")
    
    # Sequential edges
    workflow.add_edge("research_discovery", "booking_logistics")
    workflow.add_edge("booking_logistics", "planning_optimization")
    workflow.add_edge("planning_optimization", END)
    
    # Compile the graph
    app = workflow.compile()
    
    logger.info("LangGraph workflow created successfully")
    return app


async def run_travel_planning_workflow(
    trip_plan_id: str,
    travel_request_md: str,
    destination: str
) -> dict:
    """
    Run the complete travel planning workflow.
    
    Args:
        trip_plan_id: Unique trip plan identifier
        travel_request_md: Markdown formatted travel request
        destination: Destination name
    
    Returns:
        Final state dictionary with all results
    """
    logger.info(f"Starting travel planning workflow for trip: {trip_plan_id}")
    
    # Create the graph
    app = create_travel_planning_graph()
    
    # Initialize state
    initial_state: TravelPlanState = {
        "trip_plan_id": trip_plan_id,
        "travel_request_md": travel_request_md,
        "destination": destination,
        "research_results": None,
        "booking_results": None,
        "itinerary": None,
        "budget_analysis": None,
        "final_response": None,
        "current_step": "Initializing workflow",
        "errors": []
    }
    
    try:
        # Run the workflow
        logger.info("Executing LangGraph workflow")
        final_state = await app.ainvoke(initial_state)
        
        # Compile final response
        final_response = {
            "trip_plan_id": trip_plan_id,
            "research_results": final_state.get("research_results"),
            "booking_results": final_state.get("booking_results"),
            "itinerary": final_state.get("itinerary"),
            "budget_analysis": final_state.get("budget_analysis"),
            "current_step": final_state.get("current_step"),
            "errors": final_state.get("errors", [])
        }
        
        final_state["final_response"] = final_response
        
        logger.info(f"Workflow completed for trip: {trip_plan_id}")
        return final_state
        
    except Exception as e:
        logger.error(f"Error in workflow execution: {e}")
        initial_state["errors"].append(str(e))
        initial_state["current_step"] = f"Workflow failed: {str(e)}"
        raise

