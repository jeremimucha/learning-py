import math


class Vector:

    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector({self.x!r}, {self.y!r}"

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        # Slower implementation but more correct "by definition"
        # return bool(abs(self))
        # Magnitude will be > 0 if either x or y are non-0
        return bool(self.x or self.y)

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y

    def __mul__(self, scalar):
        return Vector(scalar.x * scalar, self.y * scalar)
    