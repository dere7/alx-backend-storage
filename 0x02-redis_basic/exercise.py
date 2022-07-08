#!/usr/bin/env python3
"""contains Cache class"""
from typing import Union, Callable, Any, Optional
from uuid import uuid4
import functools
import redis
import json


def count_calls(method: Callable) -> Callable:
    """counts a method calls"""
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incrby(key, 1)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """store the history of inputs and outputs for a fun"""
    key = method.__qualname__

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(key + ':inputs', *args)
        result = method(self, *args, **kwargs)
        self._redis.rpush(key + ':outputs', result)
        return result
    return wrapper


def replay(method: Callable) -> Callable:
    """display the history of calls of particular function"""
    key = method.__qualname__
    r = redis.Redis()
    print('{} was called {} times:'.format(key, r.get(key).decode('utf-8')))
    inputs = []
    for i in r.lrange(key + ':inputs', 0, -1):
        value = i.decode('utf-8')
        if value.isdigit():
            value = json.loads(value)
        inputs.append(value)

    outputs = [i.decode('utf-8') for i in r.lrange(key + ':outputs', 0, -1)]
    for inputs, outputs in zip(inputs, outputs):
        print('{}(*({!r},)) -> {}'.format(key, inputs, outputs))


class Cache:
    """used to manage cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores data in redis using the random key"""
        id = str(uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """gets values form redis for given key"""
        value = self._redis.get(key)
        if value and fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """gets string value for given key"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """gets string value for given key"""
        return self.get(key, int)
