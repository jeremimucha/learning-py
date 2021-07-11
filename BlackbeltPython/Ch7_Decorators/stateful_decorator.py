#! /usr/bin/env python


# A decorator doesn't have to be a function - it just needs to be callable,
import functools

class CountCalls:
    def __init__(self, func):
        self._func = func
        self.called = 0

    def __call__(self, *args, **kwargs):
        self.called += 1
        return self._func(*args, **kwargs)

@CountCalls
def print_hello():
    print("hello")

    