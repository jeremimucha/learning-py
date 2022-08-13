#!/usr/bin/env python3


# since Python 3.9 dictionaries support `|` and `|=` operators.
# They perform the same operation they would on sets.

def demo_dict_operator_or():
    d1 = {'a': 1, 'b': 3}
    d2 = {'a': 2, 'b': 4, 'c': 6}
    print(f"{d1 | d2}")
    d1 |= d2
    print(d1)
