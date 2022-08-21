#!/usr/bin/env python3


from typing import cast

def find_first_str(a: list[object]) -> str:
    index = next(i for i, x in enumerate(a) if isinstance(x, str))
    # We only get here if there's at least on string
    # typechecker needs to be guided here, that the type is `str`
    # an not `object`.
    return cast(str, a[index])



if __name__ == '__main__':
    pass
