#!/usr/bin/env python3


# Generator functions can be implemented both as class members, and as free functions.
# If the sole purpose of a class is to implement a generator, it might be better
# to just replace it with a generator function.


class ArithmeticProgression:

    def __init__(self, begin, step, end=None):
        self.begin = begin
        self.step = step
        self.end = end  # None -> 'infinite' series
    
    def __iter__(self):
        result_type = type(self.begin + self.step)
        result = result_type(self.begin)
        forever = self.end is None
        index = 0
        while forever or result < self.end:
            yield result
            index += 1
            result = self.begin + self.step * index


def arithmetic_progression_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0
    while forever or result < end:
        yield result
        index += 1
        result = begin + step * index


# pythons `itertools` module provides many convenience generator functions.
import itertools

def arithprog_gen(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(first, step)   # infinite range
    if end is None:
        return ap_gen
    return itertools.takewhile(lambda n: n < end, ap_gen)


if __name__ == '__main__':
    pass
