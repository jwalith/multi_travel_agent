# Travel Planner LangGraph

A modern travel planning system using LangGraph framework with 3 consolidated agents, AWS Bedrock for LLM, and free APIs only.

## Architecture

- **3-Agent System**: Research & Discovery, Booking & Logistics, Planning & Optimization
- **LangGraph Framework**: State-based workflow orchestration
- **AWS Bedrock**: Claude models for AI agents
- **Free APIs**: DuckDuckGo, Wikipedia, BeautifulSoup (no paid services)

## Setup

1. Install dependencies:
```bash
pip install -r backend/requirements.txt
```

2. Configure AWS credentials (already configured):
```bash
# AWS credentials should be in ~/.aws/credentials or environment variables
export AWS_REGION=us-east-1
```

3. Run the service:
```bash
cd backend
python main.py
```

## Project Structure

```
backend/
├── agents/          # LangGraph agents and workflow
├── config/          # Configuration (Bedrock, AWS services)
├── tools/           # Free API tools (DuckDuckGo, Wikipedia, etc.)
├── models/          # Data models
└── services/        # Business logic
```

## Features

- Free APIs only (except AWS Bedrock)
- AWS services integration (S3, Lambda, CloudWatch)
- 3-agent consolidated architecture
- LangGraph state management
- Latest package versions (no version pins)

