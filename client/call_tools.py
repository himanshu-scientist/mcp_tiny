# call_tools.py
import asyncio
import tool_utils

async def call_tool_by_name(tool_name: str, input_data: dict):
    client = tool_utils.get_client()
    async with client:
        result = await client.call_tool(tool_name, input_data)
        print(f"Result from '{tool_name}': {result}")
        print('--'*20)

# if __name__ == "__main__":
#     # Example usage
#     asyncio.run(call_tool_by_name("add", {"a": 8, "b": 13}))
#     asyncio.run(call_tool_by_name("multiply", {"a": 10, "b": 22}))
#     asyncio.run(call_tool_by_name("reverse_string", {"s": "Hello, World!"}))
#     asyncio.run(call_tool_by_name("count_words", {"s": "This is a test string."}))
