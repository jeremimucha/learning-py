#!/usr/bin/env python3
import collections


# Preffer to subclass base classes defined in the `collections`
# module, rather than builtin types like `dict`.


# In contrast to subclassing `dict` this implementation is simpler and more consistent,
# we can be sure that all assignemtns/insertions pass through our __setitem__,
# and all getters pass through __getitem__ that calls __missing__ if appropriate.
class StrKeyDict(collections.UserDict):

    # UserDict holds a `dict` instance as `self.data`
    
    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]
    
    def __contains__(self, key):
        return str(key) in self.data
    
    def __setitem__(self, key, item):
        self.data[str(key)] = item


