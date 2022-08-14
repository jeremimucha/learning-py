#!/usr/bin/env python3

from numbers import Integral
from typing import List, TypeVar


class Averager():

    T = TypeVar('T', int, float)

    def __init__(self) -> None:
        self.series = []

    def __call__(self, new_value: T) -> float:
        self.series.append(new_value)
        total = sum(self.series)
        return total / len(self.series)


# We could achieve the same using a closure.
# This implementation, however, is not optimal,
# we could be just storing the ``count`` and running ``total``.
# We'll do that next, using the ``nonlocal`` keyword.
def make_averager():
    series = []

    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total / len(series)
    
    return averager


# Better averager implementation
def better_averager():
    count = 0
    total = 0

    def averager(new_value):
        # Without the ``nonlocal`` declaration, ``count`` and ``total``
        # would have been local variables (leading to exception in this case)
        nonlocal count, total
        count += 1
        total += new_value
        return total / count


if __name__ == '__main__':
    avg = Averager()
    favg = make_averager()
    for i in range(10, 13):
        print(avg(i))
        print(favg(i))

