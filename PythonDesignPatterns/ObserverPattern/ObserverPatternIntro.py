#! python3


class Subject:
    def __init__(self):
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def notify_all(self, *args, **kwargs):
        for observer in self._observers:
            observer.notify(self, *args, **kwargs)


class Observer1:
    def __init__(self, subject):
        subject.register(self)

    def notify(self, subject, *args):
        print(type(self).__name__, ":: Got", args, 'From', subject)

class Observer2:
    def __init__(self, subject):
        subject.register(self)

    def notify(self, subject, *args):
        print(type(self).__name__, ":: Got", args, 'From', subject)

subject = Subject()
observer1 = Observer1(subject)
observer2 = Observer2(subject)
subject.notify_all('notification')
