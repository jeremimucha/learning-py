#! python3


# basic example of a metaclass

class MyIntMeta(type):
    def __call__(cls, *args, **kwargs):
        print("**** Instantiating MyIntMeta ****", args, kwargs)
        return type.__call__(cls, *args, *kwargs)

class myint(metaclass=MyIntMeta):
    def __init__(self, x, y):
        self.x = x
        self.y = y

i = myint(4, 5)
print(i)
print(type(i))


class MetaSingleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Logger(metaclass=MetaSingleton):
    pass

logger1 = Logger()
logger2 = Logger()
print(logger1)
print(logger2)
