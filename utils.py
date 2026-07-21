"""
Utility functions for the bot
"""

import re
from datetime import datetime
from typing import Optional

def format_date(date) -> str:
    """Format a date object to a readable string"""
    if hasattr(date, 'strftime'):
        return date.strftime('%Y-%m-%d %H:%M:%S')
    return str(date)

def get_user_mention(user) -> str:
    """Get a formatted user mention"""
    if user.username:
        return f"@{user.username}"
    return f"[{user.first_name}](tg://user?id={user.id})"

def is_admin(update) -> bool:
    """Check if user is an admin (simplified)"""
    # This is a placeholder - proper implementation in handlers.py
    return False

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection"""
    # Remove any markdown or special characters that could be harmful
    text = re.sub(r'[<>]', '', text)
    return text.strip()

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length"""
    if len(text) > max_length:
        return text[:max_length] + '...'
    return text

def is_valid_username(username: str) -> bool:
    """Check if a username is valid"""
    if not username:
        return False
    # Username must start with @ or letter, contain only letters, numbers, underscore
    pattern = r'^@?[a-zA-Z][a-zA-Z0-9_]{4,31}$'
    return bool(re.match(pattern, username))
