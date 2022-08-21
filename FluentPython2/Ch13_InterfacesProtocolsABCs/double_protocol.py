#!/usr/bin/env python3

from typing import TypeVar, Protocol


T = TypeVar('T')
class Repeatable(Protocol):
    def __mul__(self: T, repeat_count: int) -> T: ...


RT = TypeVar('RT', bound=Repeatable)
def double(x: RT) -> RT:
    return x * 2

