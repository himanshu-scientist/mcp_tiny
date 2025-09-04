from typing import Annotated
from pydantic import Field


def add(
    a: Annotated[float, Field(description="First addend")],
    b: Annotated[float, Field(description="Second addend")],
) -> float:
    """Add two numbers and return the sum."""
    return a + b

def multiply(
    a: Annotated[float, Field(description="Multiplicand, can be integer or float")],
    b: Annotated[float, Field(description="Multiplier, can be float")],
) -> float:
    """Multiply two numbers and return the product."""
    return a * b
