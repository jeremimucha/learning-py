#!/usr/bin/env python3


from collections.abc import Iterator
import itertools

def fibonacci() -> Iterator[int]:
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


if __name__ == '__main__':
    fib = fibonacci()
    for _ in range(11):
        print(next(fib))

    for val in itertools.takewhile(lambda x: x < 42, fibonacci()):
        print(val)
