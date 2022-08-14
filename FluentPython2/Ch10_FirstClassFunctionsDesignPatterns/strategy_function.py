#!/usr/bin/env python3

from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, NamedTuple, Optional


class Customer(NamedTuple):
    name: str
    fidelity: int


class LineItem(NamedTuple):
    product: str
    quantity: int
    price: Decimal

    def total(self) -> Decimal:
        return self.price * self.quantity

@dataclass(frozen=True)
class Order:    # the Context
    customer: Customer
    cart: Sequence[LineItem]
    promotion: Optional[Callable[['Order'], Decimal]] = None

    def total(self) -> Decimal:
        totals = (item.total() for item in self.cart)
        return sum(totals, start=Decimal(0))

    def due(self) -> Decimal:
        if self.promotion is None:
            discount = Decimal(0)
        else:
            discount = self.promotion(self)
        return self.total() - discount

    def __repr__(self):
        return f'<Order total: {self.total():.2f} due: {self.due():.2f}>'



def fidelity_promo(order: Order) -> Decimal:     # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""
    rate = Decimal('0.05')
    if order.customer.fidelity >= 1000:
        return order.total() * rate
    return Decimal(0)


def bulk_item_promo(order: Order):     # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


def large_order_promo(order: Order):
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)


# This is a maintenence burder - we'd need to remember to manually add new promotion strategies here.
# See `promo_globals.py` and `promo_inspect.py` for automated approach alternatives.
promos = [fidelity_promo, bulk_item_promo, large_order_promo]

def best_promo(order: Order):
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)


if __name__ == '__main__':
    joe = Customer('John Doe', 0)
    ann = Customer('Ann Smith', 1100)
    cart = (LineItem('banana', 4, Decimal('.5')),
            LineItem('apple', 10, Decimal('1.5')),
            LineItem('watermelon', 5, Decimal(5)))
    joe_order = Order(joe, cart, fidelity_promo)
    ann_order = Order(ann, cart, fidelity_promo)
    print(joe_order)
    print(ann_order)
    banana_cart = (LineItem('banana', 30, Decimal('.5')),
                    LineItem('apple', 10, Decimal('1.5')))
    banana_order = Order(joe, banana_cart, bulk_item_promo)
    print(banana_order)

    best_joe = Order(joe, banana_cart,  best_promo)
    best_ann = Order(ann, banana_cart, best_promo)
    print(best_joe)
    print(best_ann)
