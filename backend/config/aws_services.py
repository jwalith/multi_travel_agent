"""AWS services configuration."""

import os
import boto3
from loguru import logger
from typing import Optional


class AWSServices:
    """AWS services client initialization."""
    
    def __init__(self):
        self.region = os.getenv('AWS_REGION', 'us-east-1')
    
    def get_s3_client(self):
        """Get S3 client for caching."""
        try:
            return boto3.client('s3', region_name=self.region)
        except Exception as e:
            logger.warning(f"Failed to create S3 client: {e}")
            return None
    
    def get_lambda_client(self):
        """Get Lambda client for serverless functions."""
        try:
            return boto3.client('lambda', region_name=self.region)
        except Exception as e:
            logger.warning(f"Failed to create Lambda client: {e}")
            return None
    
    def get_dynamodb_client(self):
        """Get DynamoDB client."""
        try:
            return boto3.client('dynamodb', region_name=self.region)
        except Exception as e:
            logger.warning(f"Failed to create DynamoDB client: {e}")
            return None
    
    def get_cloudwatch_client(self):
        """Get CloudWatch client for logging."""
        try:
            return boto3.client('logs', region_name=self.region)
        except Exception as e:
            logger.warning(f"Failed to create CloudWatch client: {e}")
            return None


# Global AWS services instance
aws_services = AWSServices()

