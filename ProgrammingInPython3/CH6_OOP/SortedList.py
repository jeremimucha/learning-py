#! python3


# default sorting function #
# =========================================================================== #
_identity = lambda x: x
# =========================================================================== #


# SortedList #
# =========================================================================== #
class SortedList:

    def __init__(self, sequence=None, key=None):
        self._key = key or _identity
        assert hasattr(self._key, "__call__")
        if sequence is None:
            self._list = []
        elif (isinstance(sequence, SortedList) and
              sequence.key == self._key):
            self._list = sequence._list[:]
        else:
            self._list = sorted(list(sequence), key=self._key)

    @property
    def key(self):
        return self._key
    
    def add(self, value):
        index = self._bisect_left(value)
        if index == len(self._list):
            self._list.append(value)
        else:
            self._list.insert(index, value)

    def _bisect_left(self, value):
        key = self._key(value)
        left, right = 0, len(self._list)
        while left < right:
            middle = (left + right) // 2
            if self._key(self._list[middle]) < key:
                left = middle + 1
            else:
                right = middle
        return left

    def remove(self, value):
        index = self._bisect_left(value)
        if index < len(self._list) and self._list[index] == value:
            del self._list[index]
        else:
            raise ValueError("{0}.remove(x): x not in list".format(
                            self.__class__.__name__))

    def remove_every(self, value):
        count = 0
        index = self._bisect_left(value)
        while(index < len(self._list) and self._list[index] == value):
            del self._list[index]
            count += 1
        return count

    def count(self, value):
        count = 0
        index = self._bisect_left(value)
        while(index < len(self._list) and self._list[index] == value):
            index += 1
            count += 1
        return count

    def index(self, value):
        index = self._bisect_left(value)
        if index < len(self._list) and self._list[index] == value:
            return index
        raise ValueError("{0}.index(x): x not in list".format(
                        self.__class__.__name__))

    def __delitem__(self, index):
        del self._list[index]

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index):
        raise TypeError("use add() to insert a value and rely on the list to "
                        "put it in the right place")

    def __iter__(self):
        return iter(self._list)

    def __reversed__(self):
        return reversed(self._list)

    def __contains__(self, value):
        index = self._bisect_left(value)
        return (index < len(self._list) and self._list[index] == value)

    def clear(self):
        self._list = []

    def pop(self, index=-1):
        return self._list.pop(index)

    def __len__(self):
        return len(self._list)

    def __str__(self):
        return str(self._list)

    def copy(self):
        return SortedList(self, self._key)

    __copy__ = copy

    
# =========================================================================== #
