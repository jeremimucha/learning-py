#! python3


class Borg:
    _shared_state = {'1': '2'}
    def __init__(self):
        self.x = 1
        self.__dict__ = self._shared_state
        
class Borg_2:
    _shared_state = {}
    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj

if __name__ == '__main__':
    b = Borg()
    b1 = Borg()
    b.x = 4

    print("Borg Object 'b': ", b) # b and b1 are distinct objects
    print("Borg Object 'b1': ", b1)
    print("Object State 'b1': ", b.__dict__) # b and b1 share same state
    print("Object State 'b1': ", b1.__dict__)

    b = Borg_2()
    b1 = Borg_2()
    b.x = 4

    print("Borg Object 'b': ", b) # b and b1 are distinct objects
    print("Borg Object 'b1': ", b1)
    print("Object State 'b1': ", b.__dict__) # b and b1 share same state
    print("Object State 'b1': ", b1.__dict__)