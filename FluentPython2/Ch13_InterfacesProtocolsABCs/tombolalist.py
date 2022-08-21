#!/usr/bin/env python3

# Classes that effectively implement an ABC's interface,
# but do not directly inherit from it, can still `register`,
# as implementers of that interface.
# The registration is not checked, however instances of the class
# will still return True for isinstance() checks.
# This is known as "virtual subclassing".


from random import randrange

from tombola import Tombola

# Implement the Tombola ABC with the help of subclassing from builtin `list`.
# We can still declare that we're satisfying the Tombola interface, by registering.
# This is however unchecked.
@Tombola.register
class TomboList(list):

    def pick(self):
        if self:
            position = randrange(len(self))
            return self.pop(position)
        else:
            raise LookupError('pop from empty TomboList')
    
    load = list.extend

    def loaded(self):
        return bool(self)
    
    def inspect(self):
        return tuple(self)


# Alternatively, instead of using the @Tombola.register
# decorator we could register by calling:
# Tombola.register(TomboList)



if __name__ == '__main__':
    pass
