#!/usr/bin/env python3
"""
Exercise file for Cache class
"""
import redis
import uuid
from typing import Union, Callable, Optional
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number of calls to a method.
    It increments the count in Redis every time the method is called.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the call count
        and then calls the original method.
        """
        # Create the key for counting calls, using the method's qualified name
        key = method.__qualname__
        # Increment the call count in Redis
        self._redis.incr(key)
        # Call the original method and return its result
        return method(self, *args, **kwargs)

    return wrapper

class Cache:
    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key, store the input data in Redis,
        and return the key.
        """
        key = str(uuid.uuid4())  # Generate a random UUID key
        self._redis.set(key, data)  # Store the data in Redis
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> Union[str, bytes, int, None]:
        """
        Retrieve data from Redis and optionally apply
        a conversion function 'fn'.
        If the key does not exist, return None.
        """
        # Retrieve the data from Redis (returns bytes or None)
        data = self._redis.get(key)
        if data is None:
            return None  # Return None if the key does not exist
        if fn:
            # Apply the callable conversion function if provided
            return fn(data)
        return data  # Default behavior: return the raw data (as bytes)

    def get_str(self, key: str) -> Optional[str]:
        """
        Automatically decode the retrieved data as a UTF-8 string.
        """
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Automatically convert the retrieved data to an integer.
        """
        return self.get(key, fn=int)

if __name__ == "__main__":
    cache = Cache()

    # Store values and print the count of store method calls
    cache.store(b"first")
    print(cache.get(cache.store.__qualname__))  # Output should be b'1'

    cache.store(b"second")
    cache.store(b"third")
    print(cache.get(cache.store.__qualname__))  # Output should be b'3'
