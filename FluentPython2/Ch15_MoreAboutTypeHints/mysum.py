#!/usr/bin/env python3


import functools
import operator
from collections.abc import Iterable
from typing import overload, Union, TypeVar


T = TypeVar('T')
S = TypeVar('S')


@overload
def sum(it: Iterable[T]) -> Union[T, int]: ...
@overload
def sum(it: Iterable[T], /, start: S) -> Union[T, S]: ...

def sum(it, /, start=0):
    return functools.reduce(operator.add, it, start)


if __name__ == '__main__':
    pass
