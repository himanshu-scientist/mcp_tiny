# tools/text_tools.py

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]

def count_words(s: str) -> int:
    """Count the number of words in a string."""
    return len(s.split())
