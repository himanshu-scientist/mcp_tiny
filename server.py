# server.py
import logging
import sys
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
@mcp.tool(tags=["Mathematical operation"],enabled=True)
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
@mcp.tool(tags=["Mathematical operation"],enabled=True)
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
@mcp.tool(tags=["String operation"],enabled=True)
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
@mcp.tool(tags=["String operation"],enabled=True)
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
@mcp.tool(tags=["GenAI Operation"],enabled=True)
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
@mcp.tool(tags=["GenAI Operation"],enabled=True)
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





@mcp.tool(tags=["Data Analysis"],enabled=True)
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


@mcp.tool(tags=["web-scraping", "firecrawl"],enabled=True)
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
                # "parsers": [
                #     "pdf"
                # ],                
                "onlyMainContent": True
            })
            
    except Exception as e:
        await ctx.error(f"Error during scraping: {str(e)}")
        return {"error": str(e), "status_code": 400}        

    await ctx.info("Scraping complete")
    return str(result)


@mcp.tool(tags=["aws", "s3", "file-check"],enabled=True)
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




from tools.awslabs.cost_explorer_mcp_server.comparison_handler import (
    get_cost_and_usage_comparisons,
    get_cost_comparison_drivers,
)
from tools.awslabs.cost_explorer_mcp_server.cost_usage_handler import get_cost_and_usage
from tools.awslabs.cost_explorer_mcp_server.forecasting_handler import get_cost_forecast
from tools.awslabs.cost_explorer_mcp_server.metadata_handler import (
    get_dimension_values,
    get_tag_values,
)
from tools.awslabs.cost_explorer_mcp_server.utility_handler import get_today_date
from loguru import logger




# Define server instructions
SERVER_INSTRUCTIONS = """
# AWS Cost Explorer MCP Server

## IMPORTANT: Each API call costs $0.01 - use filters and specific date ranges to minimize charges.

## Critical Rules
- Comparison periods: exactly 1 month, start on day 1 (e.g., "2025-04-01" to "2025-05-01")
- UsageQuantity: Recommended to filter by USAGE_TYPE, USAGE_TYPE_GROUP or results are meaningless
- When user says "last X months": Use complete calendar months, not partial periods
- get_cost_comparison_drivers: returns only top 10 most significant drivers

## Query Pattern Mapping

| User Query Pattern | Recommended Tool | Notes |
|-------------------|-----------------|-------|
| "What were my costs for..." | get_cost_and_usage | Use for historical cost analysis |
| "How much did I spend on..." | get_cost_and_usage | Filter by service/region as needed |
| "Show me costs by..." | get_cost_and_usage | Set group_by parameter accordingly |
| "Compare costs between..." | get_cost_and_usage_comparisons | Ensure exactly 1 month periods |
| "Why did my costs change..." | get_cost_comparison_drivers | Returns top 10 drivers only |
| "What caused my bill to..." | get_cost_comparison_drivers | Good for root cause analysis |
| "Predict/forecast my costs..." | get_cost_forecast | Works best with specific services |
| "What will I spend on..." | get_cost_forecast | Can filter by dimension |

## Cost Optimization Tips
- Always use specific date ranges rather than broad periods
- Filter by specific services when possible to reduce data processed
- For usage metrics, always filter by USAGE_TYPE or USAGE_TYPE_GROUP to get meaningful results
- Combine related questions into a single query where possible
"""

# Create FastMCP server with instructions

# Register all tools with the app
mcp.tool('get_today_date')(get_today_date)
mcp.tool('get_dimension_values')(get_dimension_values)
mcp.tool('get_tag_values')(get_tag_values)
mcp.tool('get_cost_forecast')(get_cost_forecast)
mcp.tool('get_cost_and_usage_comparisons')(get_cost_and_usage_comparisons)
mcp.tool('get_cost_comparison_drivers')(get_cost_comparison_drivers)
mcp.tool('get_cost_and_usage')(get_cost_and_usage)

if __name__ == "__main__":
    mcp.run()
