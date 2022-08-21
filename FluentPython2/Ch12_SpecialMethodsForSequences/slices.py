#!/usr/bin/env python3


class MySeq:
    def __getitem__(self, index):
        return index


def demo_slice():
    s = MySeq()
    print(s[1])     # simple indexing
    print(s[1:4])   # slicing - slice(1, 4, None) - (begin, end, stride)
    print(s[1:4:2]) # slice(1, 4, 2)

    print(s[1:4:2, 9])      # !! (slice(1,4,2), 9)
    print(s[1:4:2, 7:9])    # !! (slice(1,4,2), slice(7,9, None))

    # To help with implementation of our own slicing operators
    # we can use the ``slice().indices()`` member:
    # S.indices(len) calculate ``(start, stop, stride)``
    # of length ``len`` of the slice described by ``S``.
    s1 = slice(None, 10, 2).indices(5)
    print(s1)   # (0, 5, 2)


if __name__ == '__main__':
    pass
