#!/usr/bin/env python3


from array import array
import math


class Vector2d:
    typecode = 'd'

    def __init__(self, x, y) -> None:
        # Convert to the expected type as soon as possible,
        # catch errors and establish an invariant early.
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)

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


if __name__ == '__main__':
    pass
