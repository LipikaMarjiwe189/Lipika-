"""
utils.py
--------
Small helper functions used across the app.
Keeping them here avoids repeating code in app.py.
"""

import os
from dotenv import load_dotenv

load_dotenv()


def api_key_is_configured() -> bool:
    """
    Check whether the GEMINI_API_KEY has been set in the .env file.

    Returns:
        True  → key is present and non-empty.
        False → key is missing; features won't work.
    """
    key = os.getenv("GEMINI_API_KEY", "").strip()
    return bool(key)


def format_response(text: str) -> str:
    """
    Light cleanup of the AI response text before displaying it.
    Strips leading/trailing whitespace so the UI looks tidy.

    Args:
        text: Raw string returned by the AI.

    Returns:
        Cleaned string.
    """
    return text.strip()


def word_count(text: str) -> int:
    """
    Count the number of words in a piece of text.
    Used to give the student a quick stats line.

    Args:
        text: Any string.

    Returns:
        Integer word count.
    """
    return len(text.split())


def truncate(text: str, max_chars: int = 500) -> str:
    """
    Safely truncate long text for preview purposes.

    Args:
        text:      The full text.
        max_chars: Maximum characters to keep.

    Returns:
        Text trimmed to max_chars, with '…' appended if truncated.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "…"
