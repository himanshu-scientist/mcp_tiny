# server.py
from fastmcp import FastMCP
import fastmcp

from tools import add, multiply, reverse_string, count_words, embed_text, compare_texts
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


# Adhoc tool to demonstrate enable/disable functionality

@mcp.tool
def dynamic_tool():
    return "I am a dynamic tool."

# Disable and re-enable the tool
dynamic_tool.disable()
dynamic_tool.enable()


# if __name__ == "__main__":
#     mcp.run()
from llm_agent import call_titan_with_tools,llm_agent_call, llm_agent_call_1
from client.list_tools import list_available_tools
from client.call_tools import call_tool_by_name

@mcp.custom_route("/llm-agent", methods=["POST"])
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
        llm_output = call_titan_with_tools(user_prompt, tools)

        print('debug point 1')
        print(f"LLM Output {llm_output} from this himanshu code:")

        # Check if LLM returned a tool call
        if "TOOL_CALL" in llm_output:
            print('debug point 2')
            tool_call = llm_output.replace("TOOL_CALL:", "").strip()
            print(f"Tool call extracted: {tool_call}, debug point 3")
            # Parse tool name and args
            import re, ast
            match = re.match(r"(\w+)\((.*)\)", tool_call)
            print('debug point 4', match)
            if not match:
                return JSONResponse({"llm": llm_output, "error": "Invalid tool call format"})

            tool_name = match.group(1)
            print('debug point 5', tool_name)
            tool_args_str = match.group(2)
            print('debug point 6', tool_args_str)
            try:
                tool_args = ast.literal_eval(tool_args_str)  # Safe parsing of args
                print('debug point 7', tool_args)
            except Exception as e:
                return JSONResponse({"llm": llm_output, "error": f"Error parsing tool args: {e}"})

            # Call the tool
            tool_result = await call_tool_by_name(tool_name, tool_args)
            print('debug point 7.1', tool_result)
            llm_output = llm_agent_call_1(user_prompt, tool_result)
            print('debug point 8', llm_output)
            return JSONResponse({
                "llm_response": llm_output,
                "tool_used": tool_name,
                "status": "success"
            })

        else:
            # No tool call, return the raw response
            return JSONResponse({"llm": llm_output})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
    