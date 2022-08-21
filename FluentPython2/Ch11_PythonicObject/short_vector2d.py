#!/usr/bin/env python3


from vector2d_v3 import Vector2d


# It's a common practice to derive from a class only to change class attributes.
# In this case we're changing the typecode of Vector2d, making it use less
# precissiong for each element.
class ShortVector2d(Vector2d):
    typecode = 'f'


if __name__ == '__main__':
    pass
