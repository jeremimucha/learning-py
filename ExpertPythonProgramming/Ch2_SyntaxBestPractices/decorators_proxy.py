#! usr/bin/env python3


class User:
    def __init__(self, roles):
        self.roles = roles

class Unauthorized(Exception):
    pass

def protect(role):
    def _protect(function):
        def __protect(*args, **kw):
            user = globals().get('user')
            if user is None or role not in user.roles:
                raise Unauthorized("I won't tell you")
            return function(*args, **kw)
        return __protect
    return _protect


tarek = User(('admin', 'user'))
bill = User(('user'))
class MySecrets:
    @protect('admin')
    def waffle_recipe(self):
        print('use tons of butter!')

these_are = MySecrets()
user = tarek
these_are.waffle_recipe()
user = bill
try:
    these_are.waffle_recipe()
except Unauthorized as e:
    print("caught: {}".format(repr(e)))
