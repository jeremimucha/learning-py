#!/usr/bin/env python3
from array import array
from collections import abc
import functools
import itertools
import math
from multiprocessing.sharedctypes import Value
import reprlib
import operator
from typing import Type


class Vector:
    typecode = 'd'

    def __init__(self, components) -> None:
        self._components = array(self.typecode, components)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)

    def __iter__(self):
        return iter(self._components)

    # Sequence protocol support:
    # Implementing just
    # __len__
    # __getitem__
    # allows as to index into the Vector and even slice it.
    def __len__(self):
        return len(self._components)

    # This simple implementation would support slicing, however,
    # it would decay the returned type into an ``array``,
    # thus exposing an implementation detail.
    # def __getitem__(self, index):
    #     return self._components[index]

    # Better implementation of __getitem__ - preserves typing
    def __getitem__(self, key):
        if isinstance(key, slice):
            cls = type(self)
            return cls(self._components[key])
        # operator.index() helps support "any" type for indexing.
        # It will appropriately validate if the given key type
        # can serve as an index.
        index = operator.index(key)
        return self._components[index]

    # Convenience access for the first 4 elements of a vector.
    # __getattr__ is called when an attribute is requested
    # on an instance of a class:
    # On call like ``obj.x``
    # - first instance `obj` is checked for `x`,
    # - if not found `obj.__class__` is checked (class attributes),
    # - if not found - the search goes up the inheritance graph,
    # - if still not found - __getattr__(self, 'x') is called
    __match_args__ = ('x', 'y', 'z', 't')

    def __getattr__(self, name):
        cls = type(self)
        try:
            pos = cls.__match_args__.index(name)
        except ValueError:
            pos = -1
        if 0 <= pos < len(self._components):
            return self._components[pos]
        msg = f"{cls.__name__!r} object has no attribute {name!r}"
        raise AttributeError(msg)

    # Because of the way __getattr__ works, we also need to implement
    # __setattr__ to ensure consistent behavior
    def __setattr__(self, name, value):
        cls = type(self)
        # Single-character attribute names are read-only for this class
        if len(name) == 1:
            if name in cls.__match_args__:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
        if error:
            msg = error.format(cls_name=cls.__name__, attr_name=name)
            raise AttributeError(msg)
        super().__setattr__(name, value)

    def angle(self, n):
        r = math.hypot(*self[n:])
        a = math.atan2(r, self[n-1])
        if (n == len(self) - 1) and (self[-1] < 0):
            return math.pi * 2 - a
        else:
            return a

    def angles(self):
        return (self.angle(n) for n in range(1, len(self)))

    def __format__(self, fmt_spec: str) -> str:
        if fmt_spec.endswith('h'):  # hyperspherical coordinates
            fmt_spec = fmt_spec[:-1]
            coords = itertools.chain([abs(self)], self.angles())
            outer_fmt = '<{}>'
        else:
            coords = self
            outer_fmt = '({})'
        components = (format(c, fmt_spec) for c in coords)
        return outer_fmt.format(', '.format(components))

    def __repr__(self):
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return f'Vector({components})'
    
    def __str__(self) -> str:
        return str(tuple(self))
    
    def __bytes__(self) -> bytes:
        return (bytes([ord(self.typecode)]) +
                bytes(self._components))
    
    # Non-mutating operator+
    def __add__(self, other):
        try:
            pairs = itertools.zip_longest(self, other, fillvalue=0.0)
            return Vector(a + b for a, b in pairs)
        except TypeError:
            # Causes the interpreter to try the __radd__ of the other operand
            return NotImplemented

    # Called for `other-type + this-type`
    def __radd__(self, other):
        return self + other     # defer to __add__

    # Same effect
    # __radd__ = __add__

    def __mul__(self, scalar):
        try:
            factor = float(scalar)
        except TypeError:
            return NotImplemented
        return Vector(n * scalar for n in self)
    
    def __rmul__(self, scalar):
        return self * scalar

    # Matrix multiplication - since python3.5 operator@ overloading is supported
    def __matmul__(self, other):
        if (isinstance(other, abc.Sized) and
            isinstance(other, abc.Iterable)):
            if len(self) == len(other):
                return sum(a * b for a, b in zip(self, other))
            else:
                raise ValueError('@ requires vectors of equal length.')
        else:
            return NotImplemented

    def __rmatmul__(self, other):
        return self @ other

    def __eq__(self, other) -> bool:
        # If we want to prevent comparisons against other iterable types
        if isinstance(other, Vector):
            return (len(self) == len(other) and all(a == b for a, b in zip(self, other)))
        else:
            return NotImplemented

    def __hash__(self) -> int:
        # Compute hash by xor'ing hashes of all elements of the vector
        hashes = (hash(x) for x in self._components)
        return functools.reduce(operator.xor, hashes, 0)

    def __abs__(self):
        # Requires python3.8
        return math.hypot(self.x, self.y)
        # Pre python3.8 use
        # return math.sqrt(sum(x * x for x in self))

    # Unary -operator
    def __neg__(self):
        return Vector(-x for x in self)

    # Unary +operator
    def __pos__(self):
        return Vector(self)

    # Unary ~operator
    # def __invert__(self):
    #     pass

    def __bool__(self):
        return bool(abs(self))

    # def __format__(self, fmt_spec: str = '') -> str:
    #     # Defining custom formatting specification.
    #     if fmt_spec.endswith('p'):
    #         fmt_spec = fmt_spec[:-1]
    #         coords = (abs(self), self.angle())
    #         outer_fmt = '<{}, {}>'
    #     else:
    #         coords = self
    #         outer_fmt = '({}, {})'
    #     components = (format(c, fmt_spec) for c in coords)
    #     return outer_fmt.format(*components)


if __name__ == '__main__':
    pass
