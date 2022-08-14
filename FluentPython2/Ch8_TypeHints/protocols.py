#!/usr/bin/env python3

# typing.Protocol lets us define expectation on operations supported by a type.
# This is pretty close to Concepts in C++.

from typing import Protocol, Any


# A `protocol` is a subclass of typing.Protocol
# The body of the protocol has one or more method definitions with `...` in their bodies.
class SupportsLessThan(Protocol):
    def __lt__(self, other: Any) -> bool: ...


from collections.abc import Iterable
from typing import TypeVar

LT = TypeVar('LT', bound=SupportsLessThan)

def top(series: Iterable[LT], length: int) -> list[LT]:
    ordered = sorted(series, reverse=True)
    return ordered[:length]

