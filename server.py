# server.py
from fastmcp import FastMCP
import fastmcp

from tools import add, multiply, reverse_string, count_words, embed_text, compare_texts
from client.list_tools import list_available_tools as  list_tools

from llm_agent import llm_get_expected_tool_and_format, llm_respond_user
from client.list_tools import list_available_tools
from client.call_tools import call_tool_by_name
import ast

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

@mcp.custom_route("/tool/add", methods=["POST"])
async def call_add_tool(request):
    try:
        # Extract input from request body
        data = await request.json()
        a = float(data.get("a"))
        b = float(data.get("b"))

        # Call the tool
        result = add(a, b)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    

# Custom route to call the Multiplication tool

@mcp.custom_route("/tool/multiply", methods=["POST"])
async def call_multiply_tool(request):
    try:
        # Extract input from request body
        data = await request.json()
        a = float(data.get("a"))
        b = float(data.get("b"))

        # Call the tool
        result = multiply(a, b)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    


# Custom route to call the Reversing of string  tool

@mcp.custom_route("/tool/reverse_string", methods=["POST"])
async def call_reverse_string_tool(request):
    try:
        # Extract input from request body
        data = await request.json()
        s = str(data.get("s"))
        # Call the tool
        result = reverse_string(s)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)




# Custom route to call the count_words tool

@mcp.custom_route("/tool/count_words", methods=["POST"])
async def call_count_words_tool(request):
    try:
        # Extract input from request body
        data = await request.json()
        s = str(data.get("s"))

        # Call the tool
        result = count_words(s)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    
@mcp.custom_route("/tool/embed_text", methods=["POST"])
async def call_embed_text_tool(request):
    try:
        # Extract input from request body
        data = await request.json()
        text = str(data.get("text"))

        # Call the tool
        result = embed_text(text)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)
    
@mcp.custom_route("/tool/compare_texts", methods=["POST"])
async def call_compare_texts_tool(request):
    try:
        # Extract input from request body
        data = await request.json()
        text1 = str(data.get("text1"))
        text2 = str(data.get("text2"))

        # Call the tool
        result = compare_texts(text1,text2)

        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


@mcp.custom_route("/llm_agent", methods=["POST"])
async def llm_agent_endpoint(request):
    try:
        data = await request.json()
        user_prompt = data.get("prompt")
        if not user_prompt:
            return JSONResponse({"error": "Missing prompt"}, status_code=400)
        
        tools = await list_available_tools() # Should return list of strings
        tools = tools["Available tools on this MCP server"]
        print("Tools fetched from MCP server:", tools)

        # Call Titan model
        tool_and_args = llm_get_expected_tool_and_format(user_prompt, tools)
        print('debug point 1', tool_and_args)
        if not tool_and_args.startswith('('):
            # LLM did not return a tool call, respond directly to user
            llm_output = llm_respond_user(user_prompt, tool_and_args)
            print('debug point 3', llm_output)
            return JSONResponse({
                "llm_response": llm_output,
            })
        else:
            print("LLM decided to use a tool.")

            print('type of tool_and_args', type(tool_and_args))
            tool_and_args = ast.literal_eval(tool_and_args)
            print('type of tool_and_args', type(tool_and_args))
            
            tool_result = await call_tool_by_name(*tool_and_args)
            print('debug point 2',tool_result)

            llm_output = llm_respond_user(user_prompt, tool_result)
            print('debug point 3', llm_output)
            return JSONResponse({
                    "llm_response": llm_output,
                })
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# @mcp.tool
# def dynamic_tool():
#     return "I am a dynamic tool."

# # Disable and re-enable the tool
# dynamic_tool.disable()
# dynamic_tool.enable()


    
    