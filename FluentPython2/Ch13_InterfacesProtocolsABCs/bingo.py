#!/usr/bin/env python3

import random

from tombola import Tombola


class BingoCage(Tombola):

    def __init__(self, items) -> None:
        self._randomizer = random.SystemRandom()
        self._items = []
        self.load(items)

    def load(self, items):
        self._items.extend(items)
        self._randomizer.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    # We could be lazy here and rely on default implementations
    # of `loaded` and `insepct` here,
    # but it's more runtime-efficient to impelemnt these here:

    def loaded(self):
        return bool(self._items)
    
    def inspect(self):
        return tuple(self._items)
    
    # Not required by the Tombola ABC, but extending the interface
    # further is not prohibited.
    def __call__(self):
        self.pick()


# Another approach to implementing the Tombola ABC

class LottoBlower(Tombola):

    def __init__(self, iterable) -> None:
        self._balls = list(iterable)

    def load(self, iterable):
        self._balls.extend(iterable)

    def pick(self):
        try:
            position = random.randrange(len(self._balls))
        except ValueError:
            raise LookupError('pick from empty LottoBlower')
        return self._balls.pop(position)
    
    def loaded(self):
        return bool(self._balls)
    
    def inspect(self):
        return tuple(self._balls)


if __name__ == '__main__':
    pass
