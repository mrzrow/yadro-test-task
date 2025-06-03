from random import choice
from datetime import datetime, timedelta
from string import ascii_letters, digits

from src.config.config import settings


def generate_alias() -> str:
    chars = ascii_letters + digits
    selected_chars = [choice(chars) for _ in range(settings.url.alias_length)]
    return ''.join(selected_chars)

def is_expired(created_at: datetime, expired_after: int) -> bool:
    """
    Check if the URL is expired based on the creation time and expiration duration.
    
    :param created_at: The timestamp when the URL was created.
    :param expired_after: The duration in seconds after which the URL expires.
    :return: True if the URL is expired, False otherwise.
    """
    return (created_at + timedelta(seconds=expired_after)) < datetime.now()
