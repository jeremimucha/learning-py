#!/usr/bin/env python3


# Since python3.8 parameters can be made positional-only:

# In the following signature ``a`` and ``b`` are required to be positional arguments,
# calls like ``mydivmod(a=4, b=3)`` are invalid.
# All parameters preceeding the ``/`` are positional-only.
def mydivmod(a, b, /):
    return (a // b, a % b)
