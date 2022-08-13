#!/usr/bin/env python3
from array import array


# `memoryview` - allows handling array slices without copying bytes.
# Useful for sharing memory between data-structures like PIL images
# SQLite databases, NumPy arrays, etc. without copying.


def demo_memoryview():
    octets = array('B', range(6))
    m1 = memoryview(octets)
    print(m1.tolist())

    # .cast returns a reinterpreted reference, sharing the same memory
    m2 = m1.cast('B', [2, 3])
    print(m2.tolist())

    m3 = m1.cast('B', [3, 2])
    print(m3.tolist())

    m2[1,1] = 22
    m3[1,1] = 33

    print(octets)



if __name__ == '__main__':
    demo_memoryview()
