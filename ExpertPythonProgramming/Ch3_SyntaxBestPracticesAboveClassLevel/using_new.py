#! /usr/bin/env python3

'''
__new__() is a static method responsible for creating class instances. It's called prior to
__init__(). Typically implementation of overridden __new__() invokes its superclass version using
super().__new__() with suitable arguments and modifies the instance beofere returning it.
'''

class InstanceCountingClass:
    instance_created = 0
    def __new__(cls, *args, **kwargs):
        print('__new__() called with:', cls, args, kwargs)
        instance = super().__new__(cls)
        instance.number = cls.instance_created
        cls.instance_created += 1
        return instance

    def __init__(self, attribute):
        print('__init__() called with:', self, attribute)
        self.attribute = attribute

instance1 = InstanceCountingClass('abc')
instance2 = InstanceCountingClass('xyz')
print(instance1.number)
print(instance2.number)


'''
Typically __new__() should return an instance of featured class, but it is possible that it
returns other class instances. In such cases the call to __init__ is skipped. This is useful
when there is need to modify creation behavior of immutable class instances, such as some builtins.
'''

class NonZero(int):
    def __new__(cls, value):
        return super().__new__(cls, value) if value != 0 else None

    def __init__(self, skipped_value):
        # implementation of __init__ could be skipped in this case
        # but it is left to present how it may be not called
        print("__init__() called")
        super().__init__()

print(type(NonZero(-12)))
print(type(NonZero(0)))
print(type(NonZero(3.14)))

