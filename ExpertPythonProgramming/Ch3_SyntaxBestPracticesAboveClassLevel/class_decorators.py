#! /usr/bin/env python3

'''
Classes can also be decorated. It can be considered a form of metaprogramming if some introspection
is done aswell.
'''

def short_repr(cls):
    cls.__repr__ = lambda self: super(cls, self).__repr__()[:8]
    return cls

@short_repr
class ClassWithRelativelyLongName:
    pass

print(ClassWithRelativelyLongName())


# A less criptic implementation
def parameterized_short_repr(max_width=8):
    '''Parameterized deocrator that shortens representation'''
    def parameterized(cls):
        '''Inner wrapper function that is actual decorator'''
        class ShortlyRepresented(cls):
            '''Subclass that provides decorated behavior'''
            def __repr__(self):
                return super().__repr__()[:max_width]
        return ShortlyRepresented
    return parameterized

# There is no way to preserve metadata if using class decorators this way
