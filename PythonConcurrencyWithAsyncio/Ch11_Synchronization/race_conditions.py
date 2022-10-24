#!/usr/bin/env python3

from pathlib import Path
import sys
import os
from typing import Callable
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import asyncio


# Race conditions due to non-atomic access that accur in multithreaded programming can not occur with asyncio,
# everything is running on a single thread.
#
# However, it is still possible to introduce race conditions.
# Whenever we `await` in a coroutine, the event loop can execute other coroutines at this point,
# which means that if we read some state, await, then write back the state, we introduce a race condition.

counter: int = 0


async def no_race_condition_increment():
    global counter
    await asyncio.sleep(0.01)
    counter = counter + 1


async def race_condition_increment():
    global counter
    temp_counter = counter
    temp_counter += 1
    # Race condition is possible here, since the await interleaves the read and write of the shared counter.
    await asyncio.sleep(0.01)
    # In the end if we run multiples of this coroutine at the same time,
    # the counte rwill only ever be set to 1.
    counter = temp_counter


async def increment_test_loop(increment: Callable):
    global counter
    counter = 0
    for _ in range(1000):
        tasks = [asyncio.create_task(increment()) for _ in range(100)]
        await asyncio.gather(*tasks)
        print(f'Counter is {counter}')
        assert counter == 100
        counter = 0


async def main():
    # await increment_test_loop(no_race_condition_increment)
    await increment_test_loop(race_condition_increment)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
