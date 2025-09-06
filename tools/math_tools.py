from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP, Context

mcp = FastMCP("my-server")
@mcp.tool
def add(
    a: Annotated[float, Field(description="First addend")],
    b: Annotated[float, Field(description="Second addend")],ctx
: Context
) -> float:
    """Add two numbers and return the sum."""
    result = a + b
    ctx.info("Performed addition", extra={"a": a, "b": b, "result": result})
    return result
@mcp.tool
def multiply(
    a: Annotated[float, Field(description="Multiplicand, can be integer or float")],
    b: Annotated[float, Field(description="Multiplier, can be float")],
) -> float:
    """Multiply two numbers and return the product."""
    result= a * b
    #Context.info("Performed multiplication", extra={"a": a, "b": b, "result": result})
    return result


