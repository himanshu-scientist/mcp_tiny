# tools/math/math_tools.py
from typing import Annotated
from pydantic import Field

class MathTool:
    def add(
        a: Annotated[float, Field(description="First addend")],
        b: Annotated[float, Field(description="Second addend")],
    ) -> float:
        """Add two numbers and return the sum."""
        result = a + b
        
        return result

    def multiply(
        a: Annotated[float, Field(description="Multiplicand, can be integer or float")],
        b: Annotated[float, Field(description="Multiplier, can be float")],
    ) -> float:
        """Multiply two numbers and return the product."""
        result= a * b
        return result


math_tool = MathTool()

def add(a, b):
    """Add two numbers and return the sum."""
    return math_tool.add(a, b,ctx)

def multiply(a, b):
    """Multiply two numbers and return the product."""
    return math_tool.multiply(a, b,ctx)