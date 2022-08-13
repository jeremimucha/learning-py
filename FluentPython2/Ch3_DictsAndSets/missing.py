#!/usr/bin/env python3


# Mappings rely on `__missing__` special method to determine what happens when a key is not found.


class StringKeyDict(dict):

    # !!!
    # Note that it is necessary to not only implement
    # __missing__ when subclassing, but to also implement
    # .get() and __contains__ to actually use __missing__.
    # It may also be necessary to implement __getitem__,
    # when subclassing collections.abc.Mapping, to actually
    # call __missing_.

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    
    def get(self, key, default=None):
        try:
            # Delegate to __getitem__ and thus also to __missing__
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key) -> bool:
        return key in self.keys() or str(key) in self.keys()
