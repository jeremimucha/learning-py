#! python3
from abc import ABCMeta, abstractmethod


class AbstractClass(metaclass=ABCMeta):
    def __init__(self):
        pass

    @abstractmethod
    def operation1(self):
        pass

    @abstractmethod
    def operation2(self):
        pass

    def template_method(self):
        print("Defining the Algorithim. Operation1 follows Operation2.")
        self.operation2()
        self.operation1()


class ConcreteClass(AbstractClass):
    def operation1(self):
        print("ConcreteClass:: Operation1")

    def operation2(self):
        print("ConcreteClass:: Operation2")


class Client:
    def main(self):
        self._concrete = ConcreteClass()
        self._concrete.template_method()

client = Client()
client.main()
