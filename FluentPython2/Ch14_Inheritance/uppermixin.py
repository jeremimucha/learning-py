#!/usr/bin/env python3


import collections


def _upper(key):
    try:
        return key.upper()
    except AttributeError:
        return key


# Mixin implementing four essential methods of a mapping,
# always calling super() with the key uppercased (if possible)
class UpperCaseMixin:
    def __setitem__(self, key, item):
        super().__setitem__(_upper(key), item)

    def __getitem__(self, key):
        return super().__getitem__(_upper(key))
    
    def get(self, key, default=None):
        return super().get(_upper(key), default)
    
    def __contains__(self, key):
        return super().__contains__(_upper(key))


# Using UpperCaseMixin - it must be the first class
# in the hierarchy, or at least preceed which is going to be it's `super()`.
class UpperDict(UpperCaseMixin, collections.UserDict):
    pass

class UpperCounter(UpperCaseMixin, collections.Counter):
    """Specialized `Counter` that uppercases string keys"""



if __name__ == '__main__':
    d = UpperDict([('a', 'letter A'), (2, 'digit two')])
    print(d)
    list(d.keys())
    d['b'] = 'letter B'
    print('b' in d)
