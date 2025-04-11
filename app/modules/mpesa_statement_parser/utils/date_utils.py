import re
from datetime import datetime

from app.config import settings

timezone = settings.TIMEZONE


def is_date_string(text):
    """Check if a string matches the expected date format."""
    pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
    return re.search(pattern, text)


def convert_to_number(number_str):
    """Convert a string to a number, handling commas."""
    number_str = number_str.replace(",", "")
    try:
        number_float = float(number_str)
    except ValueError:
        return None
    return round(number_float, 2)


def convert_to_datetime(date_string, format="%Y-%m-%d %H:%M:%S"):
    """
    Convert a date string to a timestamp (in milliseconds).
    Assumes the input date string is in EAT (East Africa Time).
    """
    dt = datetime.strptime(date_string, format)
    # Localize to EAT timezone
    dt = timezone.localize(dt)
    # Convert to milliseconds timestamp
    return int(dt.timestamp() * 1000)


def get_current_datetime():
    """Get the current date and time in EAT timezone."""
    return datetime.now(timezone)


def format_datetime(dt=None, format="%d %b %Y, %I:%M %p EAT"):
    """
    Format a datetime object with the specified format.
    If no datetime is provided, uses the current time in EAT.
    """
    if dt is None:
        dt = get_current_datetime()
    elif dt.tzinfo is None:
        # If datetime has no timezone, assume it's in EAT
        dt = timezone.localize(dt)
    return dt.strftime(format)
