# server.py
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logging.getLogger("fastmcp").setLevel(logging.INFO)

from fastmcp import FastMCP
from fastmcp import FastMCP, Context
from fastmcp.server.dependencies import get_context 

#from tools import add, multiply, reverse_string, count_words, embed_text, compare_texts

from tools.math.math_tools import add, multiply
from tools.text.text_tools import reverse_string, count_words
from tools.genai.genai_tools import embed_text, compare_texts

from client.list_tools import list_available_tools as  list_tools

# Register tools by passing the functions to the server constructor
mcp = FastMCP("base-ey-mcp", tools=[add, multiply, reverse_string, count_words, embed_text, compare_texts])

from starlette.responses import JSONResponse
 
@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    return JSONResponse({"desc": "Health of server is okay"})

@mcp.custom_route("/tool/list", methods=["GET"])
async def client_tool_list(request):
    aval_tools_dict=  await list_tools()
    return JSONResponse(aval_tools_dict)


# Custom route to call the addition tool

#@mcp.custom_route("/tool/add", methods=["POST"])
@mcp.tool
async def call_add_tool(request,ctx:Context):
    try:
        # Extract input from request body
        data = await request.json()
        a = float(data.get("a"))
        b = float(data.get("b"))

        # Call the tool
        #ctx=get_context(request)
        result = add(a, b,ctx)
        await ctx.info("Performed addition", extra={"a": a, "b": b, "result": result})

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    

# Custom route to call the Multiplication tool

#@mcp.custom_route("/tool/multiply", methods=["POST"])
@mcp.tool
async def call_multiply_tool(request,ctx:Context):
    try:
        # Extract input from request body
        data = await request.json()
        a = float(data.get("a"))
        b = float(data.get("b"))

        # Create context from request

        # Call the tool
        result = multiply(a, b,ctx)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    


# Custom route to call the Reversing of string  tool

#@mcp.custom_route("/tool/reverse_string", methods=["POST"])
@mcp.tool
async def call_reverse_string_tool(request,ctx:Context):
    try:
        # Extract input from request body
        data = await request.json()
        s = str(data.get("s"))
        # Call the tool
        result = reverse_string(s,ctx)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)




# Custom route to call the count_words tool

#@mcp.custom_route("/tool/count_words", methods=["POST"])
@mcp.tool
async def call_count_words_tool(request,ctx:Context):
    try:
        # Extract input from request body
        data = await request.json()
        s = str(data.get("s"))

        # Call the tool
        result = count_words(s,ctx)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    
#@mcp.custom_route("/tool/embed_text", methods=["POST"])
@mcp.tool
async def call_embed_text_tool(request,ctx:Context):
    try:
        # Extract input from request body
        data = await request.json()
        text = str(data.get("text"))

        # Call the tool
        result = embed_text(text,ctx)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    
#@mcp.custom_route("/tool/compare_texts", methods=["POST"])
@mcp.tool
async def call_compare_texts_tool(request,ctx:Context):
    try:
        # Extract input from request body
        data = await request.json()
        text1 = str(data.get("text1"))
        text2 = str(data.get("text2"))

        # Call the tool
        result = compare_texts(text1,text2,ctx)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


# Adhoc tool to demonstrate enable/disable functionality

# @mcp.tool
# def dynamic_tool():
#     """A dynamic tool that can be enabled or disabled."""
#     return "I am a dynamic tool."

# # Disable and re-enable the tool
# dynamic_tool.disable()
# dynamic_tool.enable()



@mcp.tool
async def analyze_data(data: list[float], ctx: Context) -> dict:
    """Analyze numerical data with comprehensive logging."""
    await ctx.debug("Starting analysis of numerical data")
    await ctx.info(f"Analyzing {len(data)} data points")
    
    try:
        if not data:
            await ctx.warning("Empty data list provided")
            return {"error": "Empty data list"}
        
        result = sum(data) / len(data)
        await ctx.info(f"Analysis complete, average: {result}")
        return {"average": result, "count": len(data)}
        
    except Exception as e:
        await ctx.error(f"Analysis failed: {str(e)}")
        raise

if __name__ == "__main__":
    mcp.run()
