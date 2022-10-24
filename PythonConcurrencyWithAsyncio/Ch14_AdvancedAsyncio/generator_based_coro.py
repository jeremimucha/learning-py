#!/usr/bin/env python3

import os
import asyncio
from typing import Generator


# Currently async/await are just syntactic sugar around the generator-based
# coroutines using `@asyncio.coroutine` and `yield from`.
# Note that this is depracated and will be removed in Python3.10
@asyncio.coroutine
def my_coroutine():
    print('Sleeping!')
    yield from asyncio.sleep(1)
    print('Finished!')


# We can use generators to implement the courutine concepts.
# We do this by letting one generator run until it yields,
# then running another generator, also until a yield point.

def generator(start: int, end: int):
    for i in range(start, end):
        yield i

# Run one step of the generator.
def run_generator_step(gen: Generator[int, None, None]):
    try:
        return gen.send(None)
    except StopIteration as si:
        return si.value


def run_classic_coros():
    one_to_five = generator(1, 5)
    five_to_ten = generator(5, 10)

    # Interleave execution of both generators
    while True:
        one_to_five_result = run_generator_step(one_to_five)
        five_to_ten_result = run_generator_step(five_to_ten)
        print(one_to_five_result)
        print(five_to_ten_result)

        if one_to_five_result is None and five_to_ten_result is None:
            break


# ---
# Coroutines are just syntactic sugar around yield/.send().
# We can acreate couroutines and drive them using send()

async def say_hello():
    print('Hello')

async def say_goodbye():
    print('Goodbye!')

async def meet_and_greet():
    await say_hello()
    await say_goodbye()

def drive_coros_send():
    coro = meet_and_greet()
    try:
        coro.send(None)
    except StopIteration as e:
        return e.value


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # asyncio.run(my_coroutine())
    run_classic_coros()
    drive_coros_send()
