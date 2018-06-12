#! python3
from abc import ABCMeta, abstractmethod


class Order(metaclass=ABCMeta):
    @abstractmethod
    def execute(self):
        pass


class BuyStockOrder(Order):
    def __init__(self, stock):
        self._stock = stock

    def execute(self):
        self._stock.buy()

class SellStockOrder(Order):
    def __init__(self, stock):
        self._stock = stock

    def execute(self):
        self._stock.sell()

class StockTrade:
    def buy(self):
        print("You will buy stocks.")

    def sell(self):
        print("You will sell stocks.")

class Agent:
    def __init__(self):
        self._orderQueue = []

    def placeOrder(self, order):
        self._orderQueue.append(order)
        order.execute()


if __name__ == "__main__":
    # Client
    stock = StockTrade()
    buyStock = BuyStockOrder(stock)
    sellStock = SellStockOrder(stock)

    # Invoker
    agent = Agent()
    agent.placeOrder(buyStock)
    agent.placeOrder(sellStock)
