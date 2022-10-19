#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import asyncpg

from util import delay, async_timed


# Async generator - defined by using `yield` in an `async def` coroutine.
# Instead of generating plain values, it generates coroutines that we can await until we get a result.
# Simple for loops don't work with async_generators, `async for` must be used instead,
# which internally calls anext() instead of next()
async def positive_integers_async(until: int):
    for integer in range(1, until):
        await delay(integer)
        yield integer


@async_timed()
async def main():
    async_generator = positive_integers_async(3)
    print(type(async_generator))    # class: async_generator

    async for number in async_generator:
        print(f'Got number {number}')

    # This is equivalent to the above:
    # print(await anext(async_generator))
    # print(await anext(async_generator))

if __name__ == '__main__':
    # Issue on Windows - need to use the SelectoEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
