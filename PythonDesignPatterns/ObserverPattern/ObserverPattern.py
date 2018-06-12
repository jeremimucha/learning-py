#! python3
from abc import ABCMeta, abstractmethod

class Subscriber(metaclass=ABCMeta):
    @abstractmethod
    def update(self):
        pass

class SMSSubscriber(Subscriber):
    def __init__(self, publisher):
        self._publisher = publisher
        self._publisher.attach(self)

    def update(self):
        print(type(self).__name__, self._publisher.getNews())

class EmailSubscriber(Subscriber):
    def __init__(self, publisher):
        self._publisher = publisher
        self._publisher.attach(self)

    def update(self):
        print(type(self).__name__, self._publisher.getNews())

class  AnyOtherSubscriber(Subscriber):
    def __init__(self, publisher):
        self._publisher = publisher
        self._publisher.attach(self)

    def update(self):
        print(type(self).__name__, self._publisher.getNews())

class NewsPublisher:
    def __init__(self):
        self._subscribers = []
        self._latestNews = None

    def attach(self, subscriber):
        self._subscribers.append(subscriber)

    def detach(self):
        return self._subscribers.pop()

    def subscribers(self):
        return [type(x).__name__ for x in self._subscribers]

    def notifySubscribers(self):
        for sub in self._subscribers:
            sub.update()

    def addNews(self, news):
        self._latestNews = news

    def getNews(self):
        return "Got news: ", self._latestNews

if __name__ == "__main__":
    news_publisher = NewsPublisher()

    for Subscribers in (SMSSubscriber, EmailSubscriber, AnyOtherSubscriber):
        Subscribers(news_publisher)
    print("\nSubscribers:", news_publisher.subscribers())

    news_publisher.addNews("Hello World!")
    news_publisher.notifySubscribers()

    print("\nDetached:", type(news_publisher.detach()).__name__)
    print("\nSubscribers:", news_publisher.subscribers())

    news_publisher.addNews("Second News!")
    news_publisher.notifySubscribers()
