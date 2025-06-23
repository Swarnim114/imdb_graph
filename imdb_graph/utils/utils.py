"""
Utility functions for the IMDB Movie Graph project.
This module contains general-purpose utility functions that may be used
across different parts of the application.
"""

def format_title(title, max_length=30):
    """
    Format a movie title for display by truncating if necessary.
    
    Args:
        title (str): The movie title to format
        max_length (int): Maximum length before truncating
        
    Returns:
        str: Formatted title
    """
    if len(title) > max_length:
        return title[:max_length] + "..."
    return title
