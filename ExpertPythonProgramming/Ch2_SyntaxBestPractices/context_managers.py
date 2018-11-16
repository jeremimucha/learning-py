#! /usr/bin/env python3

'''
context-managers are used to perform some initialization and cleanup in a exception safe way.
This essentially emulates RAII. From a different viewpoint context managers are equivalent to
try-finally blocks - do some initialization/acquire a resource in try, cleanup/release in finally

syntax is:

with context_manager:
    # ...

with context_manager as context:
    # use context here ...


It is implemented by providing the context manager protocol:
    __enter__(self)
    __exit__(self, exc_type, exc_value, traceback)
The three arguments are passed to __exit__ only if an exception occurs.
'''

# implementation using classes:

class ContextIllustration:
    def __enter__(self):
        print('entering context')
    def __exit__(self, exc_type, exc_value, traceback):
        print('leaving context')
        if exc_type is None:
            print('with no error')
        else:
            print('with an error {}'.format(exc_value))

with ContextIllustration():
    print("within context")

print()

try:
    with ContextIllustration():
        raise RuntimeError("raised within context")
except RuntimeError as e:
    print('error: {}'.format(e))


# implementation using contextlib.contextmanager
# __enter__ and __exit__ are provided within a single function, separated by a `yield` statement,
# which makes the function a generator
from contextlib import contextmanager
@contextmanager
def context_illustration():
    print('entering context')
    try:
        yield
    except Exception as e:
        print('leaving context')
        print('with an error {}'.format(e))
        # needs to be reraised
        raise
    else:
        print('leaving context')
        print('with no error')

print("\nusing contextmanager:")
with context_illustration():
    print('within context')

try:
    with context_illustration():
        raise RuntimeError("raised within context")
except RuntimeError as e:
    print("error: {}".format(e))

