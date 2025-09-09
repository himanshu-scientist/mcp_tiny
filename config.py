# config.py

import os

# Bedrock/LLM configuration
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-3-sonnet-20240229-v1:0")
TITAN_MODEL_ID = os.getenv("TITAN_MODEL_ID", "amazon.titan-text-express-v1")
REGION_NAME = os.getenv("REGION_NAME", "us-east-1")

# MCP server configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://127.0.0.1:8000")

# Other config values can be added here
