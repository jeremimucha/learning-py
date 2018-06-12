#! python3


class ComputerState:
    name = "state"
    allowed = []

    def switch(self, state):
        if state.name in self.allowed:
            print("Current:", self, " => switched to new state", state.name)
            self.__class__ = state
        else:
            print("Current:", self, " => switching to", state.name, "not possible.")

    def __str__(self):
        return self.name

class Off(ComputerState):
    name = "off"
    allowed = ['on']

class On(ComputerState):
    name = 'on'
    allowed = ['off', 'suspend', 'hibernate']

class Suspend(ComputerState):
    name = 'suspend'
    allowed = ['on']

class Hibernate(ComputerState):
    name = 'hibernate'
    allowed = ['on']


class Computer:
    def __init__(self, model='HP'):
        self._model = model
        self._state = Off()

    def change(self, state):
        self._state.switch(state)


if __name__ == '__main__':
    comp = Computer()
    comp.change(On)
    comp.change(Off)
    comp.change(On)
    comp.change(Suspend)
    comp.change(Hibernate)  # impossible transition
    comp.change(On)
    comp.change(Off)
