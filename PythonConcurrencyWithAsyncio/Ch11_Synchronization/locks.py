#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Lock
from util import delay


# asyncio locks are awaitables - if a coroutine tries to enter a critical secion
# but another coroutine already acquired the lock, the waiting croutine is blocked
# and will yield so that other code can run.
#
# Note that asyncio.Lock's, like many other asyncio objects, can not be global variables.
# This is because a Lock operates within the asyncio event loop. Instantiating a Lock
# globally would result in a new event loop instance being instantiated by the lock.


async def coro_a(lock: Lock):
    print('Coroutine coro_a waiting to acquire the lock')
    async with lock:
        print('Coroutine coro_a is in the critical section')
        await delay(2)
    print('Coroutine coro_a released the lock')

async def coro_b(lock: Lock):
    print('Coroutine coro_b waiting to acquire the lock')
    async with lock:
        print('Coroutine coro_b is in the critical section')
        await delay(2)
    print('Coroutine coro_b released the lock')


async def main():
    lock = Lock()
    await asyncio.gather(coro_a(lock), coro_b(lock))


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
