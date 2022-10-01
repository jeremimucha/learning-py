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

The value of the attributes managed by the properties are stored in
instance attributes, created in each ``LineItem`` instance::

# tag::LINEITEM_V2_PROP_DEMO[]
    >>> nutmeg = LineItem('Moluccan nutmeg', 8, 13.95)
    >>> nutmeg.weight, nutmeg.price  # <1>
    (8, 13.95)
    >>> nutmeg.__dict__  # <2>
    {'description': 'Moluccan nutmeg', 'weight': 8, 'price': 13.95}

# end::LINEITEM_V2_PROP_DEMO[]

"""


# An alternative to the built-in properties is to define custom properties ourselves.


# The Storage_name argument determines where the data for each proeprty is sotred;
# for the weight, the sotrage name will be 'weight'
def quantity(storage_name):

    # The first argument to the qty_getter could be named `self`,
    # but that would be strange because this is not a class body; instance refers to the LineItem
    # instance where the attribute will be stored.
    def qty_getter(instance):
        # References `storage_name`, so it will be preserved in the closure of this function;
        # the value is retrieved directly from the instance.__dict__ to bypass the property
        # and avoid an infinite recursion.
        return instance.__dict__[storage_name]

    # qty_setter also takes an `instance` and additionally the value.
    def qty_setter(instance, value):
        if value > 0:
            # Also goes directly through the __dict__
            instance.__dict__[storage_name] = value
        else:
            raise ValueError('value must be > 0')

    # Build a custom property object and return it.
    return property(qty_getter, qty_setter)


# tag::LINEITEM_V2_PROP_CLASS[]
class LineItem:
    weight = quantity('weight')  # <1>
    price = quantity('price')  # <2>

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight  # <3>
        self.price = price

    def subtotal(self):
        return self.weight * self.price  # <4>
# end::LINEITEM_V2_PROP_CLASS[]
