#! /usr/bin/env python3

'''
Python classes are themselves objects, their class/type is the builtin `type` type/metaclass.
`type` can be called - it returns a class object:
'''
def method(self):
    return 1
klass = type('MyClass', (object,), {'method': method})
instance = klass()
instance.method()
print(klass.__name__)
# This is equivalent to:
class MyClass:          # implicitly MyClass(metaclass=type)
    def method(self):
        return 1

instance2 = MyClass()
instance2.method()
print(MyClass.__name__)

'''
The `metaclass` argument is usually the `type` builtin, but it can be any callable with the same
signature, which returns another class object.
The call signature is:
type(name, bases, namespace)
* name : This is the name of class that will be stored in the __name__ attribute
* bases : This is the list of parent classes that will become the __bases__
  attribute and will be used to construct the MRO of a newly created class
* namespace : This is a namespace (mapping) with definitions for the class
  body that will become the __dict__ attribute
'''

# Common template for metaclass is:
class Metaclass(type):
    def __new__(mcs, name, bases, namespace):
        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls, name, bases, namespace, **kwargs):
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)

'''
Purpose of the methods:
* __new__(mcs, name, bases, namespace) : This is responsible for the actual
creation of the class object in the same way as it does for ordinary classes.
The first positional argument is a metaclass object. In the preceding example,
it would simply be a Metaclass . Note that mcs is the popular naming
convention for this argument.
* __prepare__(mcs, name, bases, **kwargs) : This creates an empty
namespace object. By default, it returns an empty dict , but it can be
overridden to return any other mapping type. Note that it does not accept
namespace as an argument because before calling it the namespace does
not exist.
* __init__(cls, name, bases, namespace, **kwargs) : This has the same meaning
as in ordinary classes. It can perform additional class object initialization
once it was created with __new__() . The first positional argument is now
named cls by convention to mark that this is already a created class object
(metaclass instance) and not a metaclass object. When __init__() gets
called, the class was already constructed and so this method can do less
things than the __new__() method. Implementing such a method is very
similar to using class decorators, but the main difference is that __init__()
will be called for every subclass, while class decorators are not called for
subclasses.
* __call__(cls, *args, **kwargs) : This is called when an instance of a
metaclass is called. The instance of a metaclass is a class object;
it is invoked when you create new instances of a class. This can be used to
override the default way how class instances are created and initialized.

The **kwargs can be passed to the metaclass object using extra keyword arguments
in the class definition:

class Klass (metaclass=Metaclass, extra='value'):
    pass
'''

class RevealingMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        print(mcs, "__new__ called")
        return super().__new__(mcs, name, bases, namespace)

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        print(mcs, "__prepare__ called")
        return super().__prepare__(name, bases, **kwargs)

    def __init__(cls, name, bases, namespace, **kwargs):
        print(cls, "__init__ called")
        super().__init__(name, bases, namespace)

    def __call__(cls, *args, **kwargs):
        print(cls, "__call__ called")
        return super().__call__(*args, **kwargs)

class RevealingClass(metaclass=RevealingMeta):
    def __new__(cls):
        print(cls, "__new__ called")
        return super().__new__(cls)

    def __init__(self):
        print(self, "__init__ called, counter = {}")
        super().__init__()

print('creating instance...')
instance = RevealingClass()

# This prints...
# <class '__main__.RevealingMeta'> __prepare__ called
# <class '__main__.RevealingMeta'> __new__ called
# <class '__main__.RevealingClass'> __init__ called
# creating instance...
# <class '__main__.RevealingClass'> __call__ called
# <class '__main__.RevealingClass'> __new__ called
# <__main__.RevealingClass object at 0x0000022F6C2FC668> __init__ called
