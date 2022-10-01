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
    ValueError: value must be > 0

No change was made::

    >>> raisins.weight
    10

The check is also performed on instantiation::

    >>> walnuts = LineItem('walnuts', 0, 10.00)
    Traceback (most recent call last):
        ...
    ValueError: value must be > 0

The proteced attribute can still be accessed if needed for some reason, such as
white box testing)::

    >>> raisins._LineItem__weight
    10

"""


class LineItem:

    def __init__(self, description, weight, price):
        self.description = description
        # Here the property setter is already in use, making sure
        # that no instances with negative weight can be created.
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property # decorates the getter method
    # all the methods taht implement a property share the name of the public attribute: weight.
    def weight(self):
        # The actual value is stored in a private attribute __weight
        return self.__weight

    # The decorated getter has a .setter attribute - which is also a decorator.
    @weight.setter
    def weight(self, value):
        if value > 0:
            # If the value is greater than zero, we set the private __weight.
            self.__weight = value
        else:
            # Otherwise ValueError is raised.
            raise ValueError('value must be > 0')
