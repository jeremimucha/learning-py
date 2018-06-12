#!python3


class Singleton:
    def __new__(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

if __name__ == '__main__':
    s = Singleton()
    print("Object created", s)
    s1 = Singleton()
    print("Object created", s1)
