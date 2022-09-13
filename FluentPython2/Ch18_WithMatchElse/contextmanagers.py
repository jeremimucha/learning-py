#!/usr/bin/env python3


import sys


class LookingGlass:

    def __enter__(self):
        self.original_write = sys.stdout.write
        sys.stdout.write = self.reverse_write
        return 'JABBERWOCKY'

    def reverse_write(self, text):
        self.original_write(text[::-1])
    
    def __exit__(self, exc_type, exc_value, traceback):
        sys.stdout.write = self.original_write
        if exc_type is ZeroDivisionError:
            print("Please do not divide by zero!")
            # Returning `True` from a context manager's `__exit__` method,
            # means "we handled the exception", and it stops propagating the exception.
            # Returning `False` or `None`, propagates the exception in flight.
            return True
        # Fallthrough is equivalent to returning None - thus propagating all other exceptions.



# The same functionality achieved with the `@contextmanager` decorator.
# The @contextmanager decorated function should have a single `yield` statement,
# everything before the yield statement is executed as the `__enter__` method,
# and everything after it becomes the `__exit__` method.
from contextlib import contextmanager

@contextmanager
def looking_glass():
    original_write = sys.stdout.write

    def reverse_write(text):
        return original_write(text[::-1])
    
    sys.stdout.write = reverse_write

    msg = ''
    try:
        # Any exceptions thrown inside of the body of the `with` statement
        # are propagated by `yield`, handle them or propagate further as needed.
        yield 'JABBERWOCKY'
    except ZeroDivisionError:
        msg = "Please DO NOT divide by zero!"
    finally:
        sys.stdout.write = original_write
        if msg:
            print(msg)


# Context-manager generators defined with the @contextmanager decorator
# become decorators themselves - functions decorated with it are protected
# as if executed within the body of the with statement:
@looking_glass()
def verse():
    print("The time has come")


if __name__ == '__main__':
    with LookingGlass() as mirror:
        print("Alice, Kitty and Snowdrop")
        print(mirror)
    print("Back to normal")

    print("\nOne more time")
    with looking_glass() as mirror:
        print("Alice, Kitty and Snowdrop")
        print(mirror)
    print("Back to normal again")

    print("\nDecorated verse:")
    verse()
