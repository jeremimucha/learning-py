#! /usr/bin/env python3

'''
Descriptors - are used internally to implement properties, methods, class methods, static methods
and the `super` type. They are classes that define how attributes of another class can be
accessed. A class can delegate management of an attribute to another class.

Descriptor classes are based on the `descriptor protocol` - three special methods:

*   __set__(self, obj, type=None) - called whenever the attribute is set -> setter
*   __get__(self, obj, value)     - called whenever the attribute is read -> getter
*   __delete(self, obj)           - called when `del` is invoked on the attribute

* if only __get__() is implemented then the descriptor is a `non-data descriptor`

Methods of this protocol are called by the objects __getattribute__() method:
* verifies if the attribute is a data descriptor
* if not, it checks if the attribute can be found in the __dict__ of the instance obj
* finally, it check if the attribute is a non-data descriptor on the instance obj
* Therefore the precedene is: descriptors, __dict__, non-data descriptors
'''

class RevealAccess(object):
    '''A data descriptor taht sets and returns values
       normally and prints a message logging their access.
    '''

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.name)
        return self.val

    def __set__(self, obj, val):
        print('Updating', self.name)
        self.val = val

class MyClass(object):
    x = RevealAccess(10, 'var "x"')
    y = 5

m = MyClass()
print(m.x)
m.x = 20
print(m.x)
print(m.y)
