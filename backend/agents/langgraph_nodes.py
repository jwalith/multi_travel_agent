"""LangGraph nodes for the three travel planning agents."""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain.agents import create_agent
from agents.langgraph_state import TravelPlanState
from config.llm import get_bedrock_model, invoke_agent_with_retry
from tools.duckduckgo_search import duckduckgo_search, duckduckgo_destination_search
from tools.wikipedia_search import wikipedia_search, wikipedia_destination_info
from tools.free_scraper import scrape_website
from tools.google_flight import get_google_flights
from tools.kayak_hotel import kayak_hotel_url_generator, search_kayak_hotels
from loguru import logger


def research_discovery_node(state: TravelPlanState) -> TravelPlanState:
    """
    Node 1: Research & Discovery Agent
    Combines Destination Explorer + Dining Agent
    Uses free APIs: DuckDuckGo, Wikipedia
    """
    logger.info("Running Research & Discovery Agent node")
    
    try:
        # Get Bedrock model
        model = get_bedrock_model(temperature=0.3, max_tokens=4096)
        
        # Tools are already LangChain tools (decorated with @tool), use them directly
        tools = [
            duckduckgo_destination_search,
            wikipedia_destination_info,
            duckduckgo_search,
        ]
        
        # Create messages with tool descriptions
        system_prompt = """You are a Research & Discovery Agent for travel planning.
        Your role is to research destinations and find:
        1. Tourist attractions, landmarks, and activities
        2. Restaurants and dining experiences
        3. Local culture and travel tips
        
        Available tools:
        - search_destination_attractions: Search for tourist attractions and landmarks
        - search_destination_restaurants: Search for restaurants and dining options
        - get_wikipedia_destination_info: Get comprehensive information from Wikipedia
        - general_search: General web search using DuckDuckGo
        
        Use these tools to gather comprehensive information.
        Provide detailed, well-organized research results.
        Focus on mainstream attractions and popular dining options.
        Include practical information like locations, opening hours, and recommendations.
        
        Format your output clearly with sections for:
        - Main Attractions
        - Dining Options
        - Activities & Experiences
        - Travel Tips"""
        
        query = f"""
        Please research the destination: {state.get('destination', '')}
        
        User's travel request:
        {state['travel_request_md']}
        
        Provide comprehensive research about:
        1. Top 10 tourist attractions and landmarks
        2. Top 5-10 restaurants and dining experiences
        3. Popular activities and experiences
        4. Local travel tips and cultural information
        
        IMPORTANT: You must use the available tools to search for current information.
        Call the tools with appropriate parameters to get real data.
        """
        
        # Create agent with tools using LangChain's agent
        agent = create_agent(model, tools)
        
        # Invoke agent with retry logic for throttling
        result = invoke_agent_with_retry(
            agent,
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=query)
                ]
            }
        )
        
        # Extract final response
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            # Get the last AI message
            for msg in reversed(messages):
                if hasattr(msg, "content") and msg.content:
                    output = msg.content
                    break
            else:
                output = str(messages[-1]) if messages else "No response"
        else:
            output = str(result)
        
        state["research_results"] = output
        state["current_step"] = "Research & Discovery completed"
        logger.info("Research & Discovery Agent completed successfully")
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        logger.error(f"Error in Research & Discovery node: {e}\n{error_trace}")
        state["errors"].append(f"Research error: {str(e)}")
        state["research_results"] = f"Error during research: {str(e)}"
    
    return state


def booking_logistics_node(state: TravelPlanState) -> TravelPlanState:
    """
    Node 2: Booking & Logistics Agent
    Combines Flight Search + Hotel Search
    Uses: fast-flights, Kayak scraping
    """
    logger.info("Running Booking & Logistics Agent node")
    
    try:
        # Get Bedrock model
        model = get_bedrock_model(temperature=0.3, max_tokens=4096)
        
        # Tools are already LangChain tools (decorated with @tool), use them directly
        tools = [
            get_google_flights,
            search_kayak_hotels,
            kayak_hotel_url_generator,
            scrape_website,
        ]
        
        # Create agent with tools using LangGraph's react agent
        system_prompt = """You are a Booking & Logistics Agent for travel planning.
        Your role is to find and recommend:
        1. Flight options with prices, times, and airlines
        2. Hotel accommodations with prices, ratings, and amenities
        
        Available tools:
        - search_flights: Search for flights using Google Flights
        - search_hotels: Search for hotels on Kayak
        - generate_hotel_search_url: Generate Kayak hotel search URL
        - scrape_website: Scrape website content for additional information
        
        Coordinate flight and hotel timing to ensure smooth travel.
        Consider user preferences from their travel request.
        Provide top 5 options for both flights and hotels.
        
        Format your output with:
        - Flight Recommendations (top 5)
        - Hotel Recommendations (top 5)
        - Booking coordination notes"""
        
        query = f"""
        Please find flights and hotels according to the user's travel request:
        {state['travel_request_md']}
        
        Requirements:
        1. Search for flights from starting location to destination
        2. Search for hotels at the destination
        3. Coordinate timing between flights and hotel check-in
        4. Consider user's budget, travel dates, and preferences
        
        IMPORTANT: Use the search_flights and search_hotels tools to get real data.
        Provide top 5 flight options and top 5 hotel options with details.
        """
        
        # Create agent
        agent = create_agent(model, tools)
        
        # Invoke agent with retry logic for throttling
        result = invoke_agent_with_retry(
            agent,
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=query)
                ]
            }
        )
        
        # Extract final response
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            for msg in reversed(messages):
                if hasattr(msg, "content") and msg.content:
                    output = msg.content
                    break
            else:
                output = str(messages[-1]) if messages else "No response"
        else:
            output = str(result)
        
        state["booking_results"] = output
        state["current_step"] = "Booking & Logistics completed"
        logger.info("Booking & Logistics Agent completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Booking & Logistics node: {e}")
        state["errors"].append(f"Booking error: {str(e)}")
        state["booking_results"] = f"Error during booking search: {str(e)}"
    
    return state


def planning_optimization_node(state: TravelPlanState) -> TravelPlanState:
    """
    Node 3: Planning & Optimization Agent
    Combines Itinerary Specialist + Budget Agent
    Uses: DuckDuckGo for timing info, budget calculation
    """
    logger.info("Running Planning & Optimization Agent node")
    
    try:
        # Get Bedrock model
        model = get_bedrock_model(temperature=0.3, max_tokens=4096)
        
        # Tools are already LangChain tools (decorated with @tool), use them directly
        tools = [
            duckduckgo_search,
            wikipedia_search,
            scrape_website,
        ]
        
        # Create agent with tools using LangGraph's react agent
        system_prompt = """You are a Planning & Optimization Agent for travel planning.
        Your role is to:
        1. Create detailed day-by-day itineraries
        2. Optimize budget and costs
        3. Schedule activities with proper timing
        4. Provide budget breakdown and recommendations
        
        Available tools:
        - search_timing_info: Search for operating hours, timing, and scheduling information
        - get_general_info: Get general information from Wikipedia
        - scrape_for_details: Scrape websites for detailed information
        
        Use the research and booking information provided to create a comprehensive plan.
        Structure each day with morning, afternoon, and evening activities.
        Include realistic travel times and buffer periods.
        Optimize costs while maintaining experience quality.
        
        Format your output with:
        - Day-by-Day Itinerary (detailed schedule)
        - Budget Breakdown (costs by category)
        - Budget Optimization Recommendations
        - Travel Tips and Notes"""
        
        context = f"""
        Research Results:
        {state.get('research_results', 'No research data available')}
        
        Booking Results:
        {state.get('booking_results', 'No booking data available')}
        
        User's Travel Request:
        {state['travel_request_md']}
        """
        
        query = f"""
        Create a comprehensive travel plan based on the following information:
        
        {context}
        
        Please provide:
        1. Detailed day-by-day itinerary with morning, afternoon, and evening activities
        2. Complete budget breakdown with costs for flights, hotels, activities, dining
        3. Budget optimization recommendations
        4. Practical travel tips and notes
        
        Ensure the itinerary is realistic, well-timed, and within budget constraints.
        Use tools if you need additional timing or scheduling information.
        """
        
        # Create agent
        agent = create_agent(model, tools)
        
        # Invoke agent with retry logic for throttling
        result = invoke_agent_with_retry(
            agent,
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=query)
                ]
            }
        )
        
        # Extract final response
        if isinstance(result, dict) and "messages" in result:
            messages = result["messages"]
            for msg in reversed(messages):
                if hasattr(msg, "content") and msg.content:
                    output = msg.content
                    break
            else:
                output = str(messages[-1]) if messages else "No response"
        else:
            output = str(result)
        
        # Try to extract itinerary and budget sections
        if "Itinerary" in output or "Day" in output:
            state["itinerary"] = output
        else:
            state["itinerary"] = output
        
        state["budget_analysis"] = output  # Budget info is in the same output
        state["current_step"] = "Planning & Optimization completed"
        logger.info("Planning & Optimization Agent completed successfully")
        
    except Exception as e:
        logger.error(f"Error in Planning & Optimization node: {e}")
        state["errors"].append(f"Planning error: {str(e)}")
        state["itinerary"] = f"Error during planning: {str(e)}"
        state["budget_analysis"] = f"Error during budget analysis: {str(e)}"
    
    return state

