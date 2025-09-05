from typing import Annotated
from pydantic import Field
from fastmcp import FastMCP, Context


async def add(
    a: Annotated[float, Field(description="First addend")],
    b: Annotated[float, Field(description="Second addend")], ctx: Context,
) -> float:
    """Add two numbers and return the sum."""
    await ctx.info("Performed addition", extra={"a": a, "b": b, "result": result})
    return a + b

async def multiply(
    a: Annotated[float, Field(description="Multiplicand, can be integer or float")],
    b: Annotated[float, Field(description="Multiplier, can be float")],ctx: Context,
) -> float:
    """Multiply two numbers and return the product."""
    await ctx.info("Performed multiplication", extra={"a": a, "b": b, "result": result})
    return a * b


