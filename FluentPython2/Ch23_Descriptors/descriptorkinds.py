"""
Overriding descriptor (a.k.a. data descriptor or enforced descriptor):

# tag::DESCR_KINDS_DEMO1[]

    >>> obj = Managed()  # <1>
    >>> obj.over  # <2>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> Managed.over  # <3>
    -> Overriding.__get__(<Overriding object>, None, <class Managed>)
    >>> obj.over = 7  # <4>
    -> Overriding.__set__(<Overriding object>, <Managed object>, 7)
    >>> obj.over  # <5>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
    >>> obj.__dict__['over'] = 8  # <6>
    >>> vars(obj)  # <7>
    {'over': 8}
    >>> obj.over  # <8>
    -> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)

# end::DESCR_KINDS_DEMO1[]

Overriding descriptor without ``__get__``:

(these tests are reproduced below without +ELLIPSIS directives for inclusion in the book;
look for DESCR_KINDS_DEMO2)

    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> Managed.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # doctest: +ELLIPSIS
    <descriptorkinds.OverridingNoGet object at 0x...>
    >>> obj.__dict__['over_no_get'] = 9
    >>> obj.over_no_get
    9
    >>> obj.over_no_get = 7
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get
    9

Non-overriding descriptor (a.k.a. non-data descriptor or shadowable descriptor):

# tag::DESCR_KINDS_DEMO3[]

    >>> obj = Managed()
    >>> obj.non_over  # <1>
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)
    >>> obj.non_over = 7  # <2>
    >>> obj.non_over  # <3>
    7
    >>> Managed.non_over  # <4>
    -> NonOverriding.__get__(<NonOverriding object>, None, <class Managed>)
    >>> del obj.non_over  # <5>
    >>> obj.non_over  # <6>
    -> NonOverriding.__get__(<NonOverriding object>, <Managed object>, <class Managed>)

# end::DESCR_KINDS_DEMO3[]

No descriptor type survives being overwritten on the class itself:

# tag::DESCR_KINDS_DEMO4[]

    >>> obj = Managed()  # <1>
    >>> Managed.over = 1  # <2>
    >>> Managed.over_no_get = 2
    >>> Managed.non_over = 3
    >>> obj.over, obj.over_no_get, obj.non_over  # <3>
    (1, 2, 3)

# end::DESCR_KINDS_DEMO4[]

Methods are non-overriding descriptors:

    >>> obj.spam  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x...>>
    >>> Managed.spam  # doctest: +ELLIPSIS
    <function Managed.spam at 0x...>
    >>> obj.spam()
    -> Managed.spam(<Managed object>)
    >>> Managed.spam()
    Traceback (most recent call last):
      ...
    TypeError: Managed.spam() missing 1 required positional argument: 'self'
    >>> Managed.spam(obj)
    -> Managed.spam(<Managed object>)
    >>> Managed.spam.__get__(obj)  # doctest: +ELLIPSIS
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x...>>
    >>> obj.spam.__func__ is Managed.spam
    True
    >>> obj.spam = 7
    >>> obj.spam
    7


"""

"""
NOTE: These tests are here because I can't add callouts after +ELLIPSIS
directives and if doctest runs them without +ELLIPSIS I get test failures.

# tag::DESCR_KINDS_DEMO2[]

    >>> obj.over_no_get  # <1>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> Managed.over_no_get  # <2>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> obj.over_no_get = 7  # <3>
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # <4>
    <__main__.OverridingNoGet object at 0x665bcc>
    >>> obj.__dict__['over_no_get'] = 9  # <5>
    >>> obj.over_no_get  # <6>
    9
    >>> obj.over_no_get = 7  # <7>
    -> OverridingNoGet.__set__(<OverridingNoGet object>, <Managed object>, 7)
    >>> obj.over_no_get  # <8>
    9

# end::DESCR_KINDS_DEMO2[]

Methods are non-overriding descriptors:

# tag::DESCR_KINDS_DEMO5[]

    >>> obj = Managed()
    >>> obj.spam  # <1>
    <bound method Managed.spam of <descriptorkinds.Managed object at 0x74c80c>>
    >>> Managed.spam  # <2>
    <function Managed.spam at 0x734734>
    >>> obj.spam = 7  # <3>
    >>> obj.spam
    7

# end::DESCR_KINDS_DEMO5[]

"""


### auxiliary functions for display only ###

def cls_name(obj_or_cls):
    cls = type(obj_or_cls)
    if cls is type:
        cls = obj_or_cls
    return cls.__name__.split('.')[-1]

def display(obj):
    cls = type(obj)
    if cls is type:
        return f'<class {obj.__name__}>'
    elif cls in [type(None), int]:
        return repr(obj)
    else:
        return f'<{cls_name(obj)} object>'

def print_args(name, *args):
    pseudo_args = ', '.join(display(x) for x in args)
    print(f'-> {cls_name(args[0])}.__{name}__({pseudo_args})')


### essential classes for this example ###

# Overriding descriptor class with __get__ and __set__.
#
# Descriptors implementing the __set__ method are `Overriding Descriptors`.
# Overriding Descriptors will override attempts ot assign to instance
# attributes.
# Official documentation calls these "Data descriptors" or "enforced descriptors".
# Properties are also overriding descriptors.
class Overriding:
    """a.k.a. data descriptor or enforced descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


# Overriding descriptor without a __get__ method.
# Without the __get__ method the behavior depends on the state
# of the managed instance. If the descriptor's instance namesake (storage attribute)
# has not been instantiated yet, accessing the managed attribute
# via it's name will return the descriptor instance (because the storage attribute does not exist yet).
# But after assignment, once the storage attribute is created, accessing it doesn't go through
# the descriptor isntance - since it doesn't implement the __get__ method.
# The storage attribute is shadowing the managed attribute, but only for reading.
class OverridingNoGet:
    """an overriding descriptor without ``__get__``"""

    def __set__(self, instance, value):
        print_args('set', self, instance, value)


# Non-overriding descriptor.
# A descriptor that does not implement __set__ is a nonoverriding descriptor.
# Setting an instance attribute with the same name will shadow the descriptor, rendering
# it ineffective for handling that attribute in that specific instance.
# Official documentation calls these "Nondata descriptors" or "shadowable descriptors".
# Methods and @functools.cached_property are implemented as nonoverriding descriptors!
class NonOverriding:
    """a.k.a. non-data or shadowable descriptor"""

    def __get__(self, instance, owner):
        print_args('get', self, instance, owner)


# Managed instance, using one instance of each of the descriptor calsses
class Managed:
    over = Overriding()
    over_no_get = OverridingNoGet()
    non_over = NonOverriding()

    # The `spam` method is here for comparison, because methods are also descriptors.
    def spam(self):
        print(f'-> Managed.spam({display(self)})')

