#! python3


class FuzzyBool:
    def __init__(self, value=0.0):
        self._value = value if 0.0 <= value <= 1.0 else 0.0

    def __invert__(self):
        return FuzzyBool(1.0 - self._value)

    def __and__(self, other):
        return FuzzyBool(min(self._value, other._value))

    def __iand__(self, other):
        self._value = min(self._value, other._value)
        return self

    def __or__(self, other):
        return FuzzyBool(max(self._value, other._value))

    def __ior__(self, other):
        self._value = max(self._value, other._value)
        return self

    def __bool__(self):
        return self._value > 0.5

    def __int__(self):
        return round(self._value)

    def __float__(self):
        return self._value

    def __lt__(self, other):
        return self._value < other._value

    def __le__(self, other):
        return self._value <= other._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return ("{0}({1})".format(self.__class__.__name__, self._value))

    def __str__(self):
        return str(self._value)

    def __format__(self, format_spec):
        return format(self._value, format_spec)

    @staticmethod
    def conjunction(*fuzzies):
        return FuzzyBool(min([float(x) for x in fuzzies]))

    @staticmethod
    def disjunction(*fuzzies):
        return FuzzyBool(max([float(x) for x in fuzzies]))

    
