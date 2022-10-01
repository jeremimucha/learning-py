"""

A line item for a bulk food order has description, weight and price fields::

    >>> raisins = LineItem('Golden raisins', 10, 6.95)
    >>> raisins.weight, raisins.description, raisins.price
    (10, 'Golden raisins', 6.95)

A ``subtotal`` method gives the total price for that line item::

    >>> raisins.subtotal()
    69.5

The weight of a ``LineItem`` must be greater than 0::

    >>> raisins.weight = -20
    Traceback (most recent call last):
        ...
    ValueError: weight must be > 0

Negative or 0 price is not acceptable either::

    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: price must be > 0

No change was made::

    >>> raisins.weight
    10

"""


# Descriptor is a protocol-based feature; no subclassing is needed to implement one.
class Quantity:

    def __init__(self, storage_name):
        # Each Quantity instance will have a storage_name attribute:
        # that's the name of the storage attribute to hold the value
        # in the managed instances.
        self.storage_name = storage_name

    # Called when there's an attempt to assign to the managed attribute.
    # - `self` is the descriptor instance (i.e. LineItem.weight or LineItem.price),
    # - `instance` is the managed instance (a LineItem instance),
    # - `value` is the value being assigned.
    def __set__(self, instance, value):
        if value > 0:
            # We must store the attribute value directly into __dict__;
            # calling setattr(instance, self.storage_name) would trigger
            # the __set__ method again, leading to infinite recursion.
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    # We need to implement __get__ because the name of the managed attribute may
    # not be the same as the `storage_name`.
    # E.g. the user could write
    #   class House:
    #       rooms = Quantity('number_of_rooms')
    #
    # `owner` here is a reference to the managed class. It's useful if we wanted
    # to support retrieving a class attribute - perhaps to emulate Python's
    # default behavior of retrieving a class attribute when the name is not found
    # in the instance.
    #
    # If a managed attribute is accessed via the class (and not the instance),
    # the `instance` argument receives value `None`.
    # To support introspection and metaprogramming, it's a good practice
    # to make __get__ return the descriptor instance when the managed attribute
    # is accessed directly through the class.
    def __get__(self, instance, owner):
        if instance is not None:
            return instance.__dict__[self.storage_name]
        else:
            # If the managed attribute (descriptor instance) is accessed directly
            # via class (and not class instance), just return reference to self.
            return self



class LineItem:
    weight = Quantity('weight') # descriptor instance, manages the `weight` attribute
    price = Quantity('price')   # descriptor instance, manages the `price` attribute

    # The rest of the class body is as simple and clean as the original code,
    # all the validation is done in the descriptor instances.
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
