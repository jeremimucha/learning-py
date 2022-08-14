#!/usr/bin/env python3

import time
import functools
from typing import Callable


# Alternative implementation of a parameterized decorator.
# Using a class we can be more explicit.


class clock:
    DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

    def __init__(self, fmt=DEFAULT_FMT) -> None:
        self.fmt = fmt

    def __call__(self, func) -> Callable:
        @functools.wraps(func)
        def clocked(*args, **kwargs):
            t0 = time.perf_counter()
            _result = func(*args, **kwargs)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            arg_lst = [repr(arg) for arg in args]
            arg_lst.extend(f'{k}={v!r}' for k, v in kwargs.items())
            args = ', '.join(arg_lst)
            result = repr(_result)
            print(self.fmt.format(**locals()))
            return _result
        return clocked



@clock(fmt='{name}: {elapsed}s')
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 2) + fibonacci(n - 1)


if __name__ == '__main__':
    print(fibonacci(6))
