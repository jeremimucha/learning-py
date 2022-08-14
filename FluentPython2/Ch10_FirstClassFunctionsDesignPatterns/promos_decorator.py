#!/usr/bin/env python3

from decimal import Decimal
from typing import Callable
from strategy_function import Order


# This module uses the decorator pattern to semi-automate registration of new promotion strategies.
# All promotions need to be decorated with @promotion.
# The main advantage of this pattern is that registration is explicit and extensible,
# other modules can easily define new promotion strategies.


Promotion = Callable[[Order], Decimal]
# Module-global list of promotions
promos: list[Promotion] = []


# Simple decorator that register decorated functions in the `promos` list.
# It could also possibly do some validation on the registered functions.
def promotion(promo: Promotion) -> Promotion:
    promos.append(promo)
    return promo


def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)


@promotion
def fidelity_promo(order: Order) -> Decimal:     # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity points"""
    rate = Decimal('0.05')
    if order.customer.fidelity >= 1000:
        return order.total() * rate
    return Decimal(0)


@promotion
def bulk_item_promo(order: Order):     # second Concrete Strategy
    """10% discount for each LineItem with 20 or more units"""
    discount = Decimal(0)
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * Decimal('0.1')
    return discount


@promotion
def large_order_promo(order: Order):
    """7% discount for orders with 10 or more distinct items"""
    distinct_items = {item.product for item in order.cart}
    if len(distinct_items) >= 10:
        return order.total() * Decimal('0.07')
    return Decimal(0)
