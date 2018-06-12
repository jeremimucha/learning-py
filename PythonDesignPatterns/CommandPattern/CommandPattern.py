#! python3
from abc import ABCMeta, abstractmethod


class Command(metaclass=ABCMeta):
    def __init__(self, recv):
        self._recv = recv

    def execute(self):
        pass

class ConcreteCommand(Command):
    def __init__(self, recv):
        self._recv = recv

    def execute(self):
        self._recv.action()

class Receiver:
    def action(self):
        print("Receiver Action")

class Invoker:
    def command(self, cmd):
        self._cmd = cmd

    def execute(self):
        self._cmd.execute()

if __name__ == "__main__":
    recv = Receiver()
    cmd = ConcreteCommand(recv)
    invoker = Invoker()
    invoker.command(cmd)
    invoker.execute()
