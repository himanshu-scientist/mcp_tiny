# tools/text/text_tools.py


class TextTool:
    def reverse_string(self, s: str) -> str:
        """Reverse a string."""
        reversed_str = s[::-1]
        return reversed_str


    def count_words(self, s: str) -> int:
        """Count the number of words in a string."""
        word_count = len(s.split())
        return word_count
    
text_tool = TextTool()
def reverse_string(s):
    """Reverse a string."""
    return text_tool.reverse_string(s)

def count_words(s):
    """Count the number of words in a string."""
    return text_tool.count_words(s)
