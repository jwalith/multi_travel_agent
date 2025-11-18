"""LLM configuration for LangGraph agents using AWS Bedrock."""

import os
import time
from langchain_aws import ChatBedrock
from config.bedrock import bedrock_config, BEDROCK_MODELS
from loguru import logger
from botocore.exceptions import ClientError


def get_bedrock_model(model_name: str = "claude_3_5_sonnet", temperature: float = 0.3, max_tokens: int = 4096):
    """
    Get AWS Bedrock model for LangChain with retry logic.
    
    Uses ChatBedrock which is specifically designed for AWS Bedrock models.
    This is the correct class for Bedrock, NOT OpenAI.
    
    Args:
        model_name: Key from BEDROCK_MODELS dict
        temperature: Model temperature
        max_tokens: Maximum tokens to generate
    
    Returns:
        ChatBedrock model instance (Bedrock-specific, not OpenAI)
    """
    try:
        model_id = BEDROCK_MODELS.get(model_name, BEDROCK_MODELS["claude_3_5_sonnet"])
        
        # ChatBedrock is the correct class for AWS Bedrock models
        # It automatically uses AWS credentials from boto3/environment
        model = ChatBedrock(
            model_id=model_id,
            model_kwargs={
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
        )
        
        logger.info(f"Initialized AWS Bedrock model: {model_id}")
        return model
        
    except Exception as e:
        logger.error(f"Failed to initialize Bedrock model: {e}")
        raise


def invoke_agent_with_retry(agent, input_data, max_retries: int = 5, initial_delay: float = 2.0):
    """
    Invoke agent with exponential backoff retry logic for throttling errors.
    
    Args:
        agent: LangChain agent instance
        input_data: Input data for agent.invoke()
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds (will be doubled on each retry)
    
    Returns:
        Agent response
    """
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return agent.invoke(input_data)
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', '')
            
            # Check if it's a throttling error
            if error_code == 'ThrottlingException' and attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                logger.warning(
                    f"Throttling error (attempt {attempt + 1}/{max_retries}). "
                    f"Retrying in {wait_time:.2f} seconds..."
                )
                time.sleep(wait_time)
                continue
            else:
                # Not a throttling error, or max retries reached
                logger.error(f"Bedrock API error: {e}")
                raise
        except Exception as e:
            # Check if it's a throttling exception in the error message
            error_str = str(e)
            if 'ThrottlingException' in error_str and attempt < max_retries - 1:
                wait_time = delay * (2 ** attempt)  # Exponential backoff
                logger.warning(
                    f"Throttling error detected (attempt {attempt + 1}/{max_retries}). "
                    f"Retrying in {wait_time:.2f} seconds..."
                )
                time.sleep(wait_time)
                continue
            else:
                # Other errors - don't retry
                logger.error(f"Error invoking agent: {e}")
                raise
    
    # Should never reach here, but just in case
    raise Exception("Max retries reached for agent invocation")


# Default model instance
default_model = get_bedrock_model()

