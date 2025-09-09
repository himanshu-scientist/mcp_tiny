# server.py
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logging.getLogger("fastmcp").setLevel(logging.INFO)



from dotenv import load_dotenv
import os

load_dotenv()
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-1")



import json
import boto3
from fastmcp import FastMCP, Context
from fastmcp import Client as FastMCPClient

#from tools import add, multiply, reverse_string, count_words, embed_text, compare_texts

from tools.math.math_tools import add, multiply
from tools.text.text_tools import reverse_string, count_words
from tools.genai.genai_tools import embed_text, compare_texts
from client.list_tools import list_available_tools as  list_tools

# Register tools by passing the functions to the server constructor
mcp = FastMCP("base-ey-mcp")

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
@mcp.tool(tags=["Mathematical operation"])
async def call_add_tool(a : float, b: float, ctx: Context)-> dict:
    """Add two numbers and return the sum."""
    await ctx.debug("Starting add two number")
    await ctx.info(f"Value of a and b is  {a, b}")
    try:
        # Call the tool
        result = add(a, b)
        await ctx.info("Performed addition", extra={"a": a, "b": b, "result": result})
        return {"result": result}
    except Exception as e:
        return {"error": str(e),"status_code":400}
    

# Custom route to call the Multiplication tool

#@mcp.custom_route("/tool/multiply", methods=["POST"])
@mcp.tool(tags=["Mathematical operation"])
async def call_multiply_tool(a : float, b: float, ctx: Context)-> dict:
    """Multiply two numbers and return the product."""
    try:
        # Call the tool
        result = multiply(a, b)
        ctx.info("Performed multiplication", extra={"a": a, "b": b, "result": result})

        return {"result": result}
    except Exception as e:
        ctx.error("ERROR while  Performing multiplication")
        return {"error": str(e),"status_code":400}
    


# Custom route to call the Reversing of string  tool

#@mcp.custom_route("/tool/reverse_string", methods=["POST"])
@mcp.tool(tags=["String operation"])
async def call_reverse_string_tool(s: str, ctx: Context)-> dict:
    """Reverse a string."""
    try:
        result = reverse_string(s)
        await ctx.info("Reversed string", extra={"original": s, "reversed": str(result)})
        return {"result": result}
    except Exception as e:
        await ctx.error("Error in Reversed string")
        return {"error": str(e),"status_code":400}




# Custom route to call the count_words tool

#@mcp.custom_route("/tool/count_words", methods=["POST"])
@mcp.tool(tags=["String operation"])
async def call_count_words_tool(s :str,ctx: Context)-> dict:
    """Count the number of words in a string."""
    try:
        # Call the tool
        result = count_words(s)
        await ctx.info("Counted words", extra={"input": s, "word_count": result})

        return {"result": result}
    except Exception as e:
        await ctx.error("Error in word counting")
        return {"error": str(e),"status_code":400}
    
#@mcp.custom_route("/tool/embed_text", methods=["POST"])
@mcp.tool(tags=["GenAI Operation"])
async def call_embed_text_tool(text:str,ctx: Context)->dict:
    """Return embedding of texts using Titan embeddings."""
    try:
        # Call the tool
        result = embed_text(text)
        await ctx.debug(f"Embedding length: {len(result)}")
        return {"result": list(result)}
    except Exception as e:
        await ctx.error(f"Error during embedding: {str(e)}")
        return {"error": str(e),"status_code":400}
    
#@mcp.custom_route("/tool/compare_texts", methods=["POST"])
@mcp.tool(tags=["GenAI Operation"])
async def call_compare_texts_tool(text1: str, text2:str, ctx: Context)-> dict:
    """Return cosine similarity between two texts using Titan embeddings."""
    try:
        # Call the tool
        result = compare_texts(text1,text2)
        await ctx.info("Starting comparison", extra={"text1": text1, "text2": text2})
        return {"result": result}
    except Exception as e:
        await ctx.error(f"Error during text comparison: {str(e)}")
        return {"error": str(e),"status_code":400}


# Adhoc tool to demonstrate enable/disable functionality

# @mcp.tool
# def dynamic_tool():
#     """A dynamic tool that can be enabled or disabled."""
#     return "I am a dynamic tool."

# # Disable and re-enable the tool
# dynamic_tool.disable()
# dynamic_tool.enable()



@mcp.tool(tags=["Data Analysis"])
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



# Connect to Firecrawl's remote MCP server
firecrawl_client = FastMCPClient(f"https://mcp.firecrawl.dev/{FIRECRAWL_API_KEY}/v2/sse")


@mcp.tool(tags=["web-scraping", "firecrawl"])
async def scrape_url(url: str, ctx: Context) -> str:
    """Scrape main content from a URL using Firecrawl's MCP."""
    await ctx.info(f"Scraping URL: {url}")
    await ctx.debug("Calling Firecrawl's scrape tool")
    result= None
    try:
        async with firecrawl_client:
            result = await firecrawl_client.call_tool("firecrawl_scrape", {
                "url": url,
                "formats": ["markdown"],
                "maxAge": 172800000,
                "parsers": [
                    "pdf"
                ],                
                "onlyMainContent": True
            })
            
    except Exception as e:
        await ctx.error(f"Error during scraping: {str(e)}")
        return {"error": str(e), "status_code": 400}        

    await ctx.info("Scraping complete")
    return str(result)


@mcp.tool(tags=["aws", "s3", "file-check"])
async def list_s3_files(bucket_name: str, ctx: Context) -> str:
    """List files in the specified S3 bucket."""
    await ctx.info(f"Listing files in bucket: {bucket_name}")
    await ctx.debug("Connecting to S3") 
    try:
        s3 = boto3.client(
            "s3",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
            verify=False
        )
        ctx.info("Connected to S3")
        response = s3.list_objects_v2(Bucket=bucket_name)
        if "Contents" in response:
            files = [obj["Key"] for obj in response["Contents"]]
            return "\n".join(files)
        else:
            return "No files found in bucket."
    except Exception as e:
        return f"Error: {str(e)}"





if __name__ == "__main__":
    mcp.run()
