#! python3
from abc import ABCMeta, abstractmethod


class Payment(metaclass=ABCMeta):

    @abstractmethod
    def do_pay(self):
        pass

class Bank(Payment):

    def __init__(self):
        self._card = None
        self._account = None

    def _getAccount(self):
        self._account = self._card  # assume card number is account number
        return self._account

    def _hasFunds(self):
        print("Bank:: Checking if Account", self._getAccount(), "has enough funds.")
        return True

    def setCard(self, card):
        self._card = card

    def do_pay(self):
        if self._hasFunds():
            print("Bank:: Paying the merchant")
            return True
        else:
            print("Bank:: Sorry, not enough funds!")
            return False

class DebitCard(Payment):

    def __init__(self):
        self._bank = Bank()

    def do_pay(self):
        card = input("Proxy:: Punch in Card Number: ")
        self._bank.setCard(card)
        return self._bank.do_pay()

class You:

    def __init__(self):
        print("You:: Lets buy the Denim shirt.")
        self._debitCard = DebitCard()
        self._isPurchased = None

    def make_payment(self):
        self._isPurchased = self._debitCard.do_pay()

    def __del__(self):
        if self._isPurchased:
            print("You:: Wow! Denim shirt is Mine!")
        else:
            print("You:: I should ern more.")



if __name__ == '__main__':
    you = You()
    you.make_payment()