"""Main entry point for travel planner service."""

from dotenv import load_dotenv
from loguru import logger
from config.logger import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging(console_level="INFO")

logger.info("Travel Planner LangGraph Service")
logger.info("Using AWS Bedrock for LLM")
logger.info("Using free APIs: DuckDuckGo, Wikipedia, BeautifulSoup")

# Example usage
if __name__ == "__main__":
    logger.info("Service ready. Import and use plan_service.generate_travel_plan()")

