#!/usr/bin/env python3


# Avoid subclassing builtins directly - list, dict, str, set, etc.
# Instead use the base classes from ``collections`` module:
# - UserList,
# - UserDict,
# - UserString


from collections import UserDict, UserList, UserString


class DoppleDict(UserDict):
    def __setitem__(self, key, value) -> None:
        return super().__setitem__(key, [value] * 2)


class DoppleDictBuiltin(dict):
    def __setitem__(self, k, value) -> None:
        return super().__setitem__(k, [value] * 2)


if __name__ == '__main__':
    for DD in (DoppleDict, DoppleDictBuiltin):
        dd = DD(one=1)
        print(dd)
        dd['two'] = 2
        print(dd)
        # Dict inheriting from builtin will break here.
        # The C implementation of dict is not guaranteed
        # to call its own methods, so overriding them
        # explicitly is necessary.
        dd.update(three=3)
