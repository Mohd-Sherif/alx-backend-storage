#!/usr/bin/env python3
"""
Exercise file for Cache class
"""
import redis
import uuid
from typing import Union


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
