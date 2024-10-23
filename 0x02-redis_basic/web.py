#!/usr/bin/env python3
"""
Implementing an expiring web cache and tracker
"""

import redis
import requests
from typing import Callable
import functools

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(method: Callable) -> Callable:
    """
    Decorator to cache the result of a webpage request and count how many times
    a particular URL was accessed.
    """
    @functools.wraps(method)
    def wrapper(url: str) -> str:
        # Generate Redis keys
        count_key = f"count:{url}"
        cache_key = f"cached:{url}"

        # Increment the access count for the URL
        redis_client.incr(count_key)

        # Check if the URL is already cached in Redis
        cached_page = redis_client.get(cache_key)
        if cached_page:
            return cached_page.decode('utf-8')

        # If not cached, fetch the page using the wrapped method
        page_content = method(url)

        # Cache the result in Redis with a 10-second expiration time
        redis_client.setex(cache_key, 10, page_content)

        return page_content

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Fetches the HTML content of the given URL.
    """
    response = requests.get(url)
    return response.text
