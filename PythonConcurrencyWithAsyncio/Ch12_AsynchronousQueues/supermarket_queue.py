#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Queue
from random import randrange
from typing import List


# Example demonstrating basic operation of an async Queue.

class Product:
    def __init__(self, name: str, checkout_time: float):
        self.name = name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id: int, products: List[Product]):
        self.customer_id = customer_id
        self.products = products


async def checkout_customer(queue: Queue, cashier_number: int):
    # Keep checking out customers if there are any in the queue
    while not queue.empty():
        # We know the queue is not empty, so we can get an item without waiting.
        # If the queue turns out to be empty after all, this raises and exception.
        # Internally this also increments a counter of "unfinished tasks" (.get() would as well).
        customer: Customer = queue.get_nowait()
        print(f'Cashier {cashier_number} '
              f'checking out customer '
              f'{customer.customer_id}')
        for product in customer.products:
            print(f'Cashier {cashier_number} '
                  f'checking out customer '
                  f'{customer.customer_id}\'s {product.name}')
            await asyncio.sleep(product.checkout_time)
        print(f'Cashier {cashier_number} '
              f'finished checking out customer '
              f'{customer.customer_id}')
        # Indicates that a formerly enqueued task is complete
        # A call to .join() blocks until a call to .task_done() has been made
        # for all items on the queue that have been previously .put() on the queue.
        queue.task_done()


async def main():
    customer_queue = Queue()
    all_products = [Product('beer', 2),
                    Product('bananas', .5),
                    Product('sausage', .2),
                    Product('dipers', .2),
                    ]
    for i in range(10):
        products = [all_products[randrange(len(all_products))]
                    for _ in range(randrange(10))]
        customer_queue.put_nowait(Customer(i, products))

    cashiers = [asyncio.create_task(checkout_customer(customer_queue, i))
                for i in range(3)]
        
    await asyncio.gather(customer_queue.join(), *cashiers)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
