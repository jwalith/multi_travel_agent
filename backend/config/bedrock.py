"""AWS Bedrock configuration."""

import os
import boto3
from anthropic import AnthropicBedrock
from typing import Optional
from loguru import logger


class BedrockConfig:
    """AWS Bedrock configuration and client setup."""
    
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_session_token = os.getenv('AWS_SESSION_TOKEN')
    
    def get_bedrock_runtime_client(self):
        """Get boto3 Bedrock Runtime client."""
        try:
            return boto3.client(
                service_name='bedrock-runtime',
                region_name=self.region
            )
        except Exception as e:
            logger.error(f"Failed to create Bedrock runtime client: {e}")
            raise
    
    def get_anthropic_bedrock_client(self):
        """Get Anthropic Bedrock client (for direct Claude access)."""
        try:
            return AnthropicBedrock(
                aws_region=self.region,
                aws_access_key=self.aws_access_key,
                aws_secret_key=self.aws_secret_key,
                aws_session_token=self.aws_session_token
            )
        except Exception as e:
            logger.error(f"Failed to create Anthropic Bedrock client: {e}")
            raise


# Available Bedrock models
BEDROCK_MODELS = {
    "claude_sonnet_4": "anthropic.claude-sonnet-4-20250514-v1:0",
    "claude_3_5_sonnet": "us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "claude_3_haiku": "us.anthropic.claude-3-haiku-20240307-v1:0",
    "claude_3_opus": "us.anthropic.claude-3-opus-20240229-v1:0",
}

# Global config instance
bedrock_config = BedrockConfig()

