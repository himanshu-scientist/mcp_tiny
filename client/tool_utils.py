# tool_utils.py
from fastmcp import Client

def get_client():
    return Client("http://127.0.0.1:8080/mcp")
