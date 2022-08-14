#!/usr/bin/env python3

# TypeVar helps with achieving true parameterized generic annotations in python
# much like template types.

from collections.abc import Sequence
from random import shuffle
from typing import Hashable, TypeVar


T = TypeVar('T')

def sample(population: Sequence[T], size: int) -> list[T]:
    if size < 1:
        raise ValueError('size must be >= 1')
    result = list(population)
    shuffle(result)
    return result[:size]


# TypeVar can also be restricted to support only a given set of types
from collections.abc import Iterable
from decimal import Decimal
from fractions import Fraction

NumberT = TypeVar('NumberT', float, Decimal, Fraction)
def mode(data: Iterable[NumberT]) -> NumberT:
    pass


# TypeVar can also be bounded - accepting types that support a given interface
# or satisfy a set of requirements (concept?).

from collections import Counter
from collections.abc import Hashable

HashableT = TypeVar("HashableT", bound=Hashable)

def mode(data: Iterable[HashableT]) -> HashableT:
    pairs = Counter(data).most_common(1)
    if len(pairs) == 0:
        raise ValueError('no mode for empty data')
    return pairs[0][0]
