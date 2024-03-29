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


# This is the same "Supermarker" example of using an async Queue.
# The blocking .get() and .put() calls are used this time, instead of the nonblocking .get_nowait()


class Product:
    def __init__(self, name: str, checkout_time: float):
        self.name = name
        self.checkout_time = checkout_time


class Customer:
    def __init__(self, customer_id: int, products: List[Product]):
        self.customer_id = customer_id
        self.products = products


async def checkout_customer(queue: Queue, cashier_number: int):
    # Keep checking out customers indefinitely
    while True:
        customer: Customer = await queue.get()
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
        queue.task_done()


# Generate a random customer
def generate_customer(customer_id: int) -> Customer:
    all_products = [Product('beer', 2),
                    Product('bananas', .5),
                    Product('sausage', .2),
                    Product('dipers', .2),
                    ]
    products = [all_products[randrange(len(all_products))]
                for _ in range(randrange(10))]
    return Customer(customer_id, products)


# Generate several random customers every second
async def customer_generator(queue: Queue):
    customer_count = 0

    while True:
        customers = [generate_customer(i)
                     for i in range(customer_count, customer_count + randrange(5))]
        for customer in customers:
            print('Waiting to put customer in line...')
            # .put() is the blocking counterpart to .get().
            # For bounded-size queues, .put() will block until there's enough space
            # in the queue, to actually enqueue an item.
            await queue.put(customer)
            print('Customer put in line!')
        customer_count += len(customers)
        await asyncio.sleep(1)


async def main():
    customer_queue = Queue(5)

    customer_producer = asyncio.create_task(customer_generator(customer_queue))
    cashiers = [asyncio.create_task(checkout_customer(customer_queue, i))
                for i in range(3)]
    
    await asyncio.gather(customer_producer, *cashiers)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
