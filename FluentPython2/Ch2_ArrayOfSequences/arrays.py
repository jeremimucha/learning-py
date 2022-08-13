#!/usr/bin/env python3
from array import array
from random import random


# Arrays in python can be used for number-only mutable sequences.
# - more efficient than list - essentially a C-array
# - support fast loading and saving - `.frombytes`, `.tofile`

def demo_array():
    floats = array('d', (random() for i in range(10**7)))
    print(floats[-1])

    with open('floats.bin', 'wb') as fp:
        floats.tofile(fp)
    
    floats2 = array('d')
    with open('floats.bin', 'rb') as fp:
        floats2.fromfile(fp, 10**7)
    
    print(floats2[-1])
    print(floats2 == floats)


if __name__ == '__main__':
    demo_array()
