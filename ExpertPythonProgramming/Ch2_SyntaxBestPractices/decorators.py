#! usr/bin/env python3

'''
Decorators are meant to make method/function wrapping easier and more readable
'''
# To achieve the same functionality without decorators:
class WithoutDecorators:
    def some_static_method():
        print("this is static method")
    some_static_method = staticmethod(some_static_method)

    def some_class_method(cls):
        print("this is class method")
    some_class_method = classmethod(some_class_method)

# And using decorators this becomes:
class WithDecorators:
    @staticmethod
    def some_static_method():
        print("this is static method")

    @classmethod
    def some_class_method(cls):
        print("this is class method")


# -------------------------------------------------------------------------------------------------
# A decorator is generally a named object that accepts a single argument when called
# and returns another callable. The decorator @ syntax is just syntactic sugar.
# Simplest implementation is a function which returns a subfunction  that wraps the original
# function call.

# Generic patter for a decorator as a function
def mydecorator(function):
    def wrapped(*args, **kwargs):
        # do some stuff be fore the original function gets called
        print("calling decorated function")
        result = function(*args, **kwargs)
        # do some stuff after function call and return the result
        print("decorated function called, about to return the result")
        return result
    # return wrapper as a decorated funciton
    return wrapped

# Generic pattern for a decorator as a class
class DecoratorAsClass:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args, **kwargs):
        # do some stuff be fore the original function gets called
        print("calling decorated function")
        result = self.function(*args, **kwargs)
        # do some stuff after function call and return the result
        print("decorated function called, about to return the result")
        return result

# Often decorators need to be parameterized
# Parameterizing using function syntax - just add another level of nesting
def repeat(number=3):
    '''Cause decorated function to be repeated a number of times.
    Last value of the original function call is returned as a result
    :param number: number of repetitions, 3 if not specified
    '''
    print("`repeat` decorator factory called")
    def actual_decorator(function):
        print("`actual_decorator` called with function = `{}`".format(function.__name__))
        def wrapper(*args, **kwargs):
            result = None
            print('decorated function called, about to call `{f}` {n} times'.format(
                f=function.__name__, n=number))
            for _ in range(number):
                result = function(*args, **kwargs)
            return result
        print("returning wrapped `{}`".format(function.__name__))
        return wrapper
    print("returning `actual_decorator` with `number` == 3")
    return actual_decorator

# When called initially this decorator returns the actual decorator that will take a callable
# as its parameter
@repeat(2)
def foo():
    print('foo')
print("Calling decorated `foo`")
foo()

# To avoid loosing wrapped functions metadata - mainly the __name__ and docstring,
# every decorator should be declared using the build-in `wraps()` decorated proved in the
# functools module. It ensures that the wrapped function's metada is preserved
from functools import wraps

def preserving_decorator(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        '''Internal wrapped function documentation.'''
        return function(*args, **kwargs)
    return wrapped

@preserving_decorator
def function_with_important_docstring():
    '''This is important  docstring we do not want to lose.'''
