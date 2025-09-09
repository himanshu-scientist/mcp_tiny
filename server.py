# server.py
from fastmcp import FastMCP
import fastmcp
import logging
from config import MODEL_ID, TITAN_MODEL_ID, REGION_NAME, MCP_SERVER_URL

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

from tools import add, multiply, reverse_string, count_words, embed_text, compare_texts
from client.list_tools import list_available_tools as  list_tools

from llm_agent import llm_get_expected_tool_and_format, llm_respond_user
from client.list_tools import list_available_tools
from client.call_tools import call_tool_by_name
import ast

# Register tools by passing the functions to the server constructor
# removing add, multiply tools for now
mcp = FastMCP("base-ey-mcp", tools=[ reverse_string, count_words, embed_text, compare_texts])

from starlette.responses import JSONResponse
 
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """
    Health check endpoint for MCP server.
    Returns a simple status message.
    """
    logger.info("Health check endpoint called.")
    return JSONResponse({"desc": "Health of server is okay"})

@mcp.custom_route("/tool/list", methods=["GET"])
async def client_tool_list(request):
    """
    Lists all available tools on the MCP server.
    """
    aval_tools_dict = await list_tools()
    logger.info(f"Tool list requested. Tools: {aval_tools_dict}")
    return JSONResponse(aval_tools_dict)


# Custom route to call the addition tool

@mcp.custom_route("/tool/add", methods=["POST"])
async def call_add_tool(request):
    """
    Calls the 'add' tool with two numbers.
    """
    try:
        data = await request.json()
        a = float(data.get("a"))
        b = float(data.get("b"))
        logger.info(f"Add tool called with a={a}, b={b}")
        result = add(a, b)
        logger.info(f"Add result: {result}")
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error in add tool: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)
    

# Custom route to call the Multiplication tool

@mcp.custom_route("/tool/multiply", methods=["POST"])
async def call_multiply_tool(request):
    """
    Calls the 'multiply' tool with two numbers.
    """
    try:
        data = await request.json()
        a = float(data.get("a"))
        b = float(data.get("b"))
        logger.info(f"Multiply tool called with a={a}, b={b}")
        result = multiply(a, b)
        logger.info(f"Multiply result: {result}")
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error in multiply tool: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)
    


# Custom route to call the Reversing of string  tool

@mcp.custom_route("/tool/reverse_string", methods=["POST"])
async def call_reverse_string_tool(request):
    """
    Calls the 'reverse_string' tool to reverse a string.
    """
    try:
        data = await request.json()
        s = str(data.get("s"))
        logger.info(f"Reverse string tool called with s={s}")
        result = reverse_string(s)
        logger.info(f"Reverse string result: {result}")
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error in reverse string tool: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)




# Custom route to call the count_words tool

@mcp.custom_route("/tool/count_words", methods=["POST"])
async def call_count_words_tool(request):
    """
    Calls the 'count_words' tool to count words in a string.
    """
    try:
        data = await request.json()
        s = str(data.get("s"))
        logger.info(f"Count words tool called with s={s}")
        result = count_words(s)
        logger.info(f"Count words result: {result}")
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error in count words tool: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)
    
@mcp.custom_route("/tool/embed_text", methods=["POST"])
async def call_embed_text_tool(request):
    """
    Calls the 'embed_text' tool to get text embeddings.
    """
    try:
        data = await request.json()
        text = str(data.get("text"))
        logger.info(f"Embed text tool called with text={text}")
        result = embed_text(text)
        logger.info(f"Embed text result: {result}")
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error in embed text tool: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)
    
@mcp.custom_route("/tool/compare_texts", methods=["POST"])
async def call_compare_texts_tool(request):
    """
    Calls the 'compare_texts' tool to compare two texts using embeddings.
    """
    try:
        data = await request.json()
        text1 = str(data.get("text1"))
        text2 = str(data.get("text2"))
        logger.info(f"Compare texts tool called with text1={text1}, text2={text2}")
        result = compare_texts(text1, text2)
        logger.info(f"Compare texts result: {result}")
        return JSONResponse({"result": result})
    except Exception as e:
        logger.error(f"Error in compare texts tool: {e}")
        return JSONResponse({"error": str(e)}, status_code=400)


@mcp.custom_route("/llm_agent", methods=["POST"])
async def llm_agent_endpoint(request):
    """
    Endpoint for LLM agent orchestration. Accepts a user prompt, determines if a tool should be called,
    invokes the tool if needed, and returns the LLM's response.
    """
    try:
        data = await request.json()
        user_prompt = data.get("prompt")
        if not user_prompt:
            logger.error("Missing prompt in llm_agent endpoint.")
            return JSONResponse({"error": "Missing prompt"}, status_code=400)
        tools = await list_available_tools()
        tools = tools["Available tools on this MCP server"]
        logger.info(f"Tools fetched from MCP server: {tools}")
        tool_and_args = llm_get_expected_tool_and_format(
            prompt=user_prompt,
            tools=tools,
            region_name=REGION_NAME,
            MODEL_ID=MODEL_ID
        )
        logger.info(f"Arguments and tools used: {tool_and_args}")
        if not tool_and_args.startswith('('):
            # LLM did not return a tool call, respond directly to user
            logger.info("LLM responded directly without tool call.")
            return JSONResponse({"llm_response": tool_and_args})
        else:
            logger.info("LLM decided to use a tool.")
            logger.info(f"Tools and arguments used: {tool_and_args}")
            logger.debug(f"Type of tool_and_args: {type(tool_and_args)}")
            tool_and_args = ast.literal_eval(tool_and_args)
            logger.debug(f"Type of tool_and_args after eval: {type(tool_and_args)}")
            tool_result = await call_tool_by_name(*tool_and_args)
            logger.info(f"Tool result: {tool_result}")
            llm_output = llm_respond_user(
                prompt=user_prompt,
                MODEL_ID=MODEL_ID,
                region_name=REGION_NAME,
                tool_info=tool_result
            )
            logger.info(f"Final output from LLM to user: {llm_output}")
            return JSONResponse({
                "tool_used": tool_and_args[0],
                "llm_response": llm_output,
            })
    except Exception as e:
        logger.error(f"Error in llm_agent endpoint: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)


# @mcp.tool
# def dynamic_tool():
#     return "I am a dynamic tool."

# # Disable and re-enable the tool
# dynamic_tool.disable()
# dynamic_tool.enable()


    
    