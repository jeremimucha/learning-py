#!/usr/bin/env python3


class Pixel:
    # Save memory and computation by reserving space only for the specified
    # data fileds. This make the class "unpythonic" in a sense - we're preventing,
    # instances of the class to be extensible dynamically, the `__dict__` member
    # is no longer present for classes that implement __slots__.
    __slots__ = ('x', 'y')

    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y


# Subclassing __slots__ classes doesn't mean that the deriving class also uses __slots__.
class OpenPixel(Pixel):
    pass


# If we don't want the subclass to have the __dict__ member, we need to say so explicitly:
class ClosedPixel(Pixel):
    # Declare an empty tuple - this class doesn't add any slots, but uses the base class' ones.
    __slots__ = ()


# Additional attributes can be added:
class ColorPixel(Pixel):
    __slots__ = ('color',)


if __name__ == '__main__':
    op = OpenPixel()
    print(op.__dict__)
    # Still uses the __slots__ from the base class
    op.x = 42
    print(op.__dict__)
    # But new members can be assigned and will use __dict__
    op.color = 'green'
    print(op.__dict__)
