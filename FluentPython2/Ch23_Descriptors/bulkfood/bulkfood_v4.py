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

No change was made::

    >>> raisins.weight
    10

Negative or 0 price is not acceptable either::

    >>> truffle = LineItem('White truffle', 100, 0)
    Traceback (most recent call last):
        ...
    ValueError: price must be > 0

If the descriptor is accessed in the class, the descriptor object is
returned:

    >>> LineItem.weight  # doctest: +ELLIPSIS
    <bulkfood_v4.Quantity object at 0x...>
    >>> LineItem.weight.storage_name
    'weight'

"""


class Quantity:

    # __set_name__ was added in Python3.6.
    # The interpreter calls __set_name__ on each descriptor it finds
    # in a class body - if the descriptor implements it.
    # More precisely, __set_name__ is called by type.__new__ - the constructor
    # of objects representing classes. The build-in `type` is actually a metaclass.
    #
    # Descriptors implementing __set_name__ don't need an __init__,
    # instead __set_name__ saved the name of the storage attribute.
    #
    # - self - descriptor instance,
    # - owner - the managed class,
    # - name - is the name of the attribute of owner, to which this
    #   descriptor instance was assigned in the class body of owner.
    def __set_name__(self, owner, name):
        # This is what the __init__ did in implementation without __set_name__
        self.storage_name = name

    # Same implementation as in the non-__set_name__ case.
    def __set__(self, instance, value):
        if value > 0:
            instance.__dict__[self.storage_name] = value
        else:
            msg = f'{self.storage_name} must be > 0'
            raise ValueError(msg)

    
    # __get__ isn't needed - the name of the storage attribute matches
    # the name of the managed attribute. There's no risk of a mistake,
    # missuse or malicious intent.
    # def __get__(self, instance, owner):

class LineItem:
    # Now there's no need to pass the managed attribute name to the descriptor constructor.
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
