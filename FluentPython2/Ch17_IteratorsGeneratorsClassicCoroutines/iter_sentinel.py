#!/usr/bin/env python3


# The "sentinel" form of `iter()`:
# - takes a callable and a sentinel value,
# - calls the callable repeatedly, until the sentinel value is returned
# - enountering the sentinel value causes `StopIteration` to be raised.


from random import randint


def d6():
    return randint(1, 6)


def demo_iter_with_sentinel():
    d6iter = iter(d6, 1)
    print(d6iter)
    for roll in d6iter:
        print(roll)




if __name__ == '__main__':
    demo_iter_with_sentinel()
