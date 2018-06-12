#! python3
from abc import ABCMeta, abstractmethod

class State(metaclass=ABCMeta):
    @abstractmethod
    def do_this(self):
        pass

class StartState(State):
    def do_this(self):
        print("TV Switching ON")

class StopState(State):
    def do_this(self):
        print("TV Switching OFF")

class TVContext(State):
    def __init__(self):
        self._state = None

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = state

    def do_this(self):
        self._state.do_this()

context = TVContext()
context.get_state()
start = StartState()
stop = StopState()

context.set_state(stop)
context.do_this()
