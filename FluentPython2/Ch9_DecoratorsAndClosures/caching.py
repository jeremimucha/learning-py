#!/usr/bin/env python3

import functools
from clockdeco import clock


# or functools.lru_cache
# .cache is a wrapper around lru_cache simplifying its use, but also limiting functionality.
@functools.cache
@clock
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)
    

# lru_cache (least-recently-used cache)
# accepts additional parameters:
# * maxsize=128
#   - sets the maximum number of entries to be cached
# * typed=False
#   - determines whether the results of different argument types
#     are stored separately.
@functools.lru_cache(maxsize=2**20, typed=True)
def another_fibonacci(n):
    if n < 2:
        return n
    return another_fibonacci(n - 2) + another_fibonacci(n - 1)


if __name__ == '__main__':
    print(fibonacci(6))
