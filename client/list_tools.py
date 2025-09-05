import asyncio
from client import tool_utils
from fastmcp import Client

async def list_available_tools():
    # Connect to your HTTP endpoint (streamable-http)
    client = tool_utils.get_client()
    # client = Client("http://127.0.0.1:8080/mcp")
    final_tool = []
    async with client:
        tools =  await client.list_tools()
    print(tools)
    print(type(tools))
    for t in tools:
        final_dict = {}
        print(f"{t.name} — {t.description}")
        print(f"schema: {t.inputSchema}\n")
        final_dict['name']= t.name
        final_dict['description']= t.description
        final_dict['schema']= t.inputSchema
        final_tool.append(final_dict)

    return {"Available tools on this MCP server" : final_tool}

if __name__ == "__main__":
    asyncio.run(list_available_tools())

