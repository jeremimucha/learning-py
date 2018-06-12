#! python3
from abc import ABCMeta, abstractmethod

class State(metaclass=ABCMeta):
    @abstractmethod
    def Handle(self):
        pass

    
class ConcreteStateB(State):
    def Handle(self):
        print("ConcreteStateB")

class ConcreteStateA(State):
    def Handle(self):
        print("ConcreteStateA")

class Context(State):

    def __init__(self):
        self._state = None

    def get_state(self):
        return self._state
    
    def set_state(self, state):
        self._state = state

    def Handle(self):
        self._state.Handle()

context = Context()
stateA = ConcreteStateA()
stateB = ConcreteStateB()

context.set_state(stateA)
context.Handle()
