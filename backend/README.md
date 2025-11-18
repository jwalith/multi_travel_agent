# Travel Planner

An AI-powered travel planning system that automatically researches destinations, finds flights and hotels, and creates personalized day-by-day itineraries with budget optimization. Built with LangGraph for multi-agent orchestration and AWS Bedrock for intelligent decision-making.

## Overview

This is a modern travel planning system using:
- **LangGraph** for agent orchestration
- **AWS Bedrock** (Claude models) for LLM
- **3-Agent Architecture**: Research & Discovery, Booking & Logistics, Planning & Optimization

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Architecture

### Agents

1. **Research & Discovery Agent** - Researches tourist attractions, restaurants, and local culture using free search APIs to gather comprehensive destination information.
   - Searches for attractions and restaurants
   - Uses: DuckDuckGo, Wikipedia
   - Output: Comprehensive destination research

2. **Booking & Logistics Agent** - Searches and recommends flights and hotels, coordinating timing and preferences to find the best travel options.
   - Finds flights and hotels
   - Uses: fast-flights, Kayak scraping
   - Output: Flight and hotel recommendations

3. **Planning & Optimization Agent** - Creates detailed day-by-day itineraries with realistic scheduling and budget optimization based on research and booking data.
   - Creates day-by-day itinerary
   - Optimizes budget
   - Uses: DuckDuckGo for timing info
   - Output: Complete itinerary with budget breakdown

### Workflow

```
Research & Discovery → Booking & Logistics → Planning & Optimization → END
```

## Usage

```python
from models.travel_plan import TravelPlanRequest, TravelPlanAgentRequest
from services.plan_service import generate_travel_plan

# Create request
travel_plan = TravelPlanRequest(
    destination="Paris",
    starting_location="New York",
    duration=5,
    # ... other fields
)

request = TravelPlanAgentRequest(
    trip_plan_id="trip-001",
    travel_plan=travel_plan
)

# Generate plan
result = await generate_travel_plan(request)
```

## APIs Used

- **DuckDuckGo**: Web search
- **Wikipedia**: Destination information 
- **BeautifulSoup**: Web scraping
- **fast-flights**: Flight search
- **Kayak**: Hotel search via scraping

## AWS Services

- **Bedrock**: LLM
- **S3**: Caching 
- **Lambda**: Serverless functions 
- **CloudWatch**: Logging
- **DynamoDB**: Database 

