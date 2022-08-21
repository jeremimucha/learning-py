#!/usr/bin/env python3

"""
v3 of Vector2d
- hashable
- ``match`` support


To make the Vector2d hashable, instances need to be immutable, to ensure that hashes are consistent.
Hashable types need to:
- implement __hash__(self)
- implement __eq__(self, other), that is consistent with __hash__

Pattern matching is supported by default only using keyword arguments.
To support positional matching it's necessary to implement:
- __match_args__
"""

from array import array
import math


class Vector2d:
    # Support for pattern matching.
    # Not all __init__ arguments need to be included in __match_args__,
    # if some __init__ args are optional, it might make sense to leave them out
    # of __match_args__.
    __match_args__ = ('x', 'y')
    typecode = 'd'

    def __init__(self, x, y) -> None:
        # Convert to the expected type as soon as possible,
        # catch errors and establish an invariant early.
        self.__x = float(x)
        self.__y = float(y)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    def angle(self) -> float:
        return math.atan2(self.y, self.x)

    def __iter__(self):
        return (i for i in (self.x, self.y))

    def __repr__(self):
        class_name = type(self).__name__
        return '{}({!r}, {!r})'.format(class_name, *self)
    
    def __str__(self) -> str:
        return str(tuple(self))
    
    def __bytes__(self) -> bytes:
        return (bytes([ord(self.typecode)]) +
                bytes(array(self.typecode, self)))
    
    def __eq__(self, other) -> bool:
        # easily compare element-wise by converting to tuple
        return tuple(self) == tuple(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(abs(self))

    def __format__(self, fmt_spec: str = '') -> str:
        # Defining custom formatting specification.
        if fmt_spec.endswith('p'):
            fmt_spec = fmt_spec[:-1]
            coords = (abs(self), self.angle())
            outer_fmt = '<{}, {}>'
        else:
            coords = self
            outer_fmt = '({}, {})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(*components)


def positional_pattern_demo(v: Vector2d) -> None:
    match v:
        case Vector2d(0, 0):
            print(f"{v!r} is null")
        case Vector2d(0):
            print(f"{v!r} is vertical")
        case Vector2d(_, 0):
            print(f"{v!r} is horizontal")
        case Vector2d(x, y) if x==y:
            print(f"{v!r} is diagonal")
        case _:
            print(f"{v!r} is awesome")


if __name__ == '__main__':
    pass
