#!/usr/bin/env python3
from collections import deque

# collections.deque - threadsafe double-ended queue designed
# for fast inserting and removing from both ends.


def demo_deque():
    dq = deque(range(10), maxlen=10)
    print(dq)

    dq.rotate()
    print(dq)
    dq.appendleft(-1)
    print(dq)
    dq.extend([11, 22, 33])
    print(dq)
    dq.extendleft([10, 20, 30, 40])
    print(dq)
