#! /usr/bin/env python


# Given code with some obvious duplication:
class Store_0:

    def get_food(self, username, food):
        if username != 'admin':
            raise Exception("This user is not allowed to get food.")
        return self.storage.get(food)
    
    def put_food(self, username, food):
        if username != 'admin':
            raise Exception("This user is not allowed to put food.")
        self.storage.put(food)

# It would be obvious to factor the common parts out:
def ensure_is_admin(username):
    if username != 'admin':
        raise Exception('This user is not allowed to access food.')

class Store_1:

    def get_food(self, username, food):
        ensure_is_admin(username)
        return self.storage.get(food)

    def put_food(self, username, food):
        ensure_is_admin(username)
        self.storage.put(food)


# A more pythonic solution would be to extract the precondition check into a decorator
import functools

def check_is_admin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if kwargs.get('username') != 'admin':
            raise Exception("This user is not allowed to access food.")
        return func(*args, **kwargs)
    return wrapper


class Store_2:

    @check_is_admin
    def get_food(self, username, food):
        return self.storage.get(food)

    @check_is_admin
    def put_food(self, username, food):
        self.storage.put(food)


# The decorator would be more reusable if we parameterized the user that has the access rights:

def allow_access(username):
    def check_access_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if kwargs.get('username') != username:
                raise Exception('This user is not allowed to access food.')
            return func(*args, **kwargs)
        return wrapper
    return check_access_decorator


class Store_3:

    @allow_access('admin')
    @allow_access('user123')
    def get_food(self, username, food):
        return self.storage.get(food)

    @allow_access('admin')
    @allow_access('user123')
    def put_food(self, username, food):
        self.storage.put(food)


# Until now we've assumed that the decorated function has the 'username' keyword argument,
# we could relax this restriction by allowing the 'username' to be either a keyword or a positional
# argument. This can be done with the `inspect` module
import inspect

def allow_access(username):
    def check_access_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_args = inspect.getcallargs(func, *args, **kwargs)
            if func_args.get('username') != username:
                raise Exception('This user is not allowed to access food.')
            return func(*args, **kwargs)
        return wrapper
    return check_access_decorator
