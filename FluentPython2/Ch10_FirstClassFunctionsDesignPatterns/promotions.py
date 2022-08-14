#!/usr/bin/env python3

from decimal import Decimal
from strategy_function import Order


# This module is part of an approach that automates aggregation
# of all promotion strategies.
# See `promos_inspect.py`


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
