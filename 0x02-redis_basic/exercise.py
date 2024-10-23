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

def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs
    and outputs for a function in Redis.
    It stores inputs in a Redis list with the key '<method_name>:inputs'
    and outputs in a Redis list with the key '<method_name>:outputs'.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that stores the inputs and outputs to Redis lists.
        """
        # Create Redis keys for inputs and outputs
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"
        
        # Convert args to a string format and store in Redis inputs list
        self._redis.rpush(inputs_key, str(args))
        
        # Call the original method to get the result
        result = method(self, *args, **kwargs)
        
        # Store the result in the Redis outputs list
        self._redis.rpush(outputs_key, str(result))
        
        return result

    return wrapper

class Cache:
    def __init__(self):
        """
        Initialize the Redis client and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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

    # Store values and print their UUIDs
    s1 = cache.store("first")
    print(s1)
    s2 = cache.store("secont")
    print(s2)
    s3 = cache.store("third")
    print(s3)

    # Retrieve the inputs and outputs history for the store method
    inputs = cache._redis.lrange(f"{cache.store.__qualname__}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{cache.store.__qualname__}:outputs", 0, -1)

    print("inputs: {}".format(inputs))
    print("outputs: {}".format(outputs))
