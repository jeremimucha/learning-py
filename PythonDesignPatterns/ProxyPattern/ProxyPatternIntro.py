#! python3


class Actor:
    def __init__(self):
        self._isBusy = False

    def occupied(self):
        self._isBusy = True
        print(type(self).__name__, "is occupied with current movie.");

    def available(self):
        self._isBusy = False
        print(type(self).__name__, "is free for the movie")

    def getStatus(self):
        return self._isBusy


class Agent:
    def __init__(self):
        self._principal = None

    def work(self):
        self.actor = Actor()
        if self.actor.getStatus():
            self.actor.occupied()
        else:
            self.actor.available()


if __name__ == '__main__':
    r = Agent()
    r.work()
