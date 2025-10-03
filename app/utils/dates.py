"""
Utility functions for dates and time.
"""

from datetime import datetime


def get_current_date_string() -> str:
    """
    Get the current date in a formatted string for use in agent prompts.
    
    Returns:
        str: Current date formatted as "Day, Month DD, YYYY"
    """
    now = datetime.now()
    return now.strftime("%A, %B %d, %Y") 