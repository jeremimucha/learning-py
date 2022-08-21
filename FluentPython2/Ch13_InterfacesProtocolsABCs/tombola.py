#!/usr/bin/env python3


import abc


class Tombola(abc.ABC):

    @abc.abstractmethod
    def load(self, iterable):
        """Add items from an iterable."""
        # Note that an abstractmethod can have an entirely empty body.

    @abc.abstractmethod
    def pick(self):
        """Remove item at random, returning it.
        
        This method should raise `LookupError` when the instance is empty."""

    # An ABC can provide default implementations.
    # These must rely only on the interface defined by the ABC,
    # i.e. the other concrete or abstract methods or properties.
    # This might lead to inefficient, but still correct implementations.
    def loaded(self):
        """Return `True` if there's at least 1 item, `False` otherwise."""
        return bool(self.inspect())
    
    def inspect(self):
        """Return a sorted tuple with the items currently inside."""
        items = []
        while True:
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)
        return tuple(items)


if __name__ == '__main__':
    class FakeTombola(Tombola):
        def pick(self):
            return 13
    
    try:
        f = FakeTombola()
    except TypeError as e:
        # An exception is thrown here:
        # `TypeError: Can't instantiate abstract class FakeTombola with abstract method load`
        print(e)

