#! /usr/bin/env python3

'''
Properties - built-in descriptor type that knows how to link an attribute to a set of methods
It takes four optional arguments: fget, fset, fdel, doc.
'''

class Rectangle:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    def _width_get(self):
        return self.x2 - self.x1

    def _width_set(self, value):
        self.x2 = self.x1 + value

    def _height_get(self):
        return self.y2 - self.y1
    
    def _height_set(self, value):
        self.y2 = self.y1 + value

    width = property(
        _width_get, _width_set,
        doc="rectangle width measured from left"
    )
    height = property(
        _height_get, _height_set,
        doc="rectangle height measured from top"
    )

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(
            self.__class__.__name__,
            self.x1, self.y1, self.x2, self.y2
        )

rectangle = Rectangle(10, 10, 25, 34)
print(rectangle.width, rectangle.height)

rectangle.width = 100
print(rectangle)
help(Rectangle)

# Using the decorator syntax:
class Rect:
    def __init__(self, x1, y1, x2, y2):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2

    @property
    def width(self):
        '''rectangle height measured from top'''
        return self.x2 - self.x1

    @width.setter
    def width(self, value):
        self.x2 = self.x1 + value

    @property
    def height(self):
        '''rectangle height measured from top'''
        return self.y2 - self.y1

    @height.setter
    def height(self, value):
        self.y2 = self.y1 + value

    def __repr__(self):
        return "{}({}, {}, {}, {})".format(
            self.__class__.__name__,
            self.x1, self.y1, self.x2, self.y2
        )


rect = Rect(10, 10, 25, 34)
print(rect.width, rect.height)

rect.width = 100
print(rect)
help(Rect)
