#!/usr/bin/env python3
"""
Exercise file for Cache class
"""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key, store the input data in Redis,
        and return the key.
        """
        key = str(uuid.uuid4())  # Generate a random UUID key
        self._redis.set(key, data)  # Store the data in Redis
        return key

    def get(self, key: str, fn: Optional[Callable] = None)
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
