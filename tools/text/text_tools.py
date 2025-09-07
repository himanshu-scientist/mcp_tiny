# tools/text/text_tools.py

from fastmcp import FastMCP, Context


async def reverse_string(s: str,ctx:Context) -> str:
    """Reverse a string."""
    reversed_str = s[::-1]
    #await ctx.info("Reversed string", extra={"original": s, "reversed": reversed_str})
    return reversed_str


async def count_words(s: str,ctx:Context) -> int:
    """Count the number of words in a string."""
    word_count = len(s.split())
    #await ctx.info("Counted words", extra={"input": s, "word_count": word_count})
    return word_count