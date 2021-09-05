#!/usr/bin/env python


def foo(n):
    while n != 0:
        print('before yield')
        yield n
        n -= 1
        print('after yield')
