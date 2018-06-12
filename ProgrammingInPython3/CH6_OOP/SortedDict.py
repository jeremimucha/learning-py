#! python3
import SortedList

# SortedDict #
# =========================================================================== #
class SortedDict(dict):

    def __init__(self, dictionary=None, key=None, **kwargs):
        dictionary = dictionary or {}
        super().__init__(dictionary)
        if kwargs:
            super().update(kwargs)
        self._keys = SortedList.SortedList(super().keys(), key)

    def update(self, dictionary=None, **kwargs):
        if dictionary is None:
            pass
        elif isinstance(dictionary, dict):
            super().update(dictionary)
        else:
            for key, value in dictionary.items():
                super().__setitem__(key, value)
        if kwargs:
            super().update(kwargs)
        self._keys = SortedList.SortedList(super().keys(), self._keys.key)

    @classmethod
    def fromkeys(cls, iterable, value=None, key=None):
        return cls({k: value for k in iterable}, key)

    def __setitem__(self, key, value):
        if key not in self:
            self._keys.add(key)
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        try:
            self._keys.remove(key)
        except ValueError:
            raise KeyError(key)
        return super().__delitem__(key)

    def setdefault(self, key, value=None):
        if key not in self:
            self._keys.add(key)
        return super().setdefault(key, value)

    def pop(self, key, *args):
        if key not in self:
            if len(args) == 0:
                raise KeyError(key)
            return args[0]
        self._keys.remove(key)
        return super().pop(key, args)

    def popitem(self):
        item = super().popitem()
        self._keys.remove(item[0])
        return item

    def clear(self):
        super().clear()
        self._keys.clear()

    def values(self):
        for key in self._keys:
            yield self[key]

    def items(self):
        for key in self._keys:
            yield (key, self[key])

    def __iter__(self):
        return iter(self._keys)

    keys = __iter__

    def __repr__(self):
        return object.__repr__(self)

    def __str__(self):
        return ("{" + ", ".join(["{0!r}: {1!r}".format(k, v)
                    for k, v in self.items()]) + "}")

    def copy(self):
        d = SortedDict()
        super(SortedDict, d).update(self)
        d._keys = self._keys.copy()
        return d

    __copy__ = copy

    def value_at(self, index):
        return self[self._keys[index]]

    def set_value_at(self, index, value):
        self[self._keys[index]] = value

    
# =========================================================================== #
