#!/usr/bin/env python3


class Root:
    def ping(self):
        print(f'{self}.ping() in Root')
    
    def pong(self):
        print(f'{self}.pong() in Root')

    def __repr__(self) -> str:
        cls_name = type(self).__name__
        return f'<instance of {cls_name}'
    

class A(Root):
    def ping(self):
        print(f'{self}.ping() in A')
        super().ping()
    
    def pong(self):
        print(f'{self}.pong() in A')
        super().pong()
    

class B(Root):
    def ping(self):
        print(f'{self}.ping() in B')
        super().ping()

    def pong(self):
        print(f'{self}.pong() in B')
        # B.pong() doesn't call Root.pong()
        # This is known as a `noncooperative` method,
        # and can be a source of subtle bugs.
        # It's recommented to avoid noncooperative methods.


class Leaf(A, B):
    def ping(self):
        print(f'{self}.ping() in Leaf')
        super().ping()


# Python is inherently dynamic, so the MRO may be surprising.
# U() is unrelated to Root() in anyway, but non the less
# calls super().ping() - if it is used in combination with
# classes that have a base class that does implement the
# .ping() method - it will be called accordingly with the
# inheritance hierarchy.
#
# In practice this could be considered a `mixin`.
class U():
    def ping(self):
        print(f'{self}.ping() in U')
        super().ping()

# Note the inheritance order - U needs to preceed A,
# otherwise U.ping() will never be called.
class LeafUA(U, A):
    def ping(self):
        print(f'{self}.ping() in LeafUA')
        super().ping()



if __name__ == '__main__':
    l = Leaf()
    l.ping()
    l.pong()

    lua = LeafUA()
    lua.ping()
    lua.pong()
