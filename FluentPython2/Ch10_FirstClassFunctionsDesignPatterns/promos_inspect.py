#!/usr/bin/env python3

import inspect
from decimal import Decimal

from strategy_function import Order
import promotions

# Here we assume that the functions defined in the `promotions` module
# are all only promotion strategies. If this requirement isn't satisfied at some point,
# than `best_promo` would break. This would likely need to be asserted with further
# introspection or testing.
promos = [func for _, func in inspect.getmembers(promotions, inspect.isfunction)]


def best_promo(order: Order) -> Decimal:
    """Compute the best discount available"""
    return max(promo(order) for promo in promos)


if __name__ == '__main__':
    pass
