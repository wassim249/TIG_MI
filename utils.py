import re

def remove_colors(text):
    """Remove color names from text
    Args:
        text (str): Text to remove color names from
    Returns:
        str: Text with color names removed
    """
    # List of common color names
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'brown', 'black', 'white', 'gray']

    # Create a regex pattern to match color names
    pattern = re.compile(r'\b(?:' + '|'.join(colors) + r')\b', flags=re.IGNORECASE)

    # Replace color names with an empty string
    result = re.sub(pattern, '', text)

    return result