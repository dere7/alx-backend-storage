#!/usr/bin/env python3
""" Main file """

import time
import redis
from web import get_page
Cache = __import__('exercise').Cache
replay = __import__('exercise').replay

cache = Cache()

s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store(12)
print(s3)

inputs = cache._redis.lrange(
    "{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange(
    "{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

replay(cache.store)

print('-'*100)
url = 'http://google.com'
r = redis.Redis()

# count is 0 before request
assert r.get('count:'+url) is None
get_page(url)
# count is 1 after request
assert int(r.get('count:'+url)) == 1
# cached after requst
assert int(r.exists('content:'+url)) == 1
time.sleep(10)
# cache cleared after 10s
assert int(r.exists('content:'+url)) == 0
r.flushdb()
