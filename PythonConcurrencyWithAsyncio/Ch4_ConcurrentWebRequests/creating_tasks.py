#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import aiohttp
from aiohttp import ClientSession

from util import (
    async_timed,
    delay
)

# Creating many tasks can become less than trivial.
# Using simple for loops or list comprehension has a multitude of drawbacks:
# - We must manually manage our tasks, remembering to separately create and await them.
# - When one of the coroutines finishes long before the others, we'll be trapped,
#   waiting for all other coroutines to be done.
#   We might want to be more responsive in some scenarios - processing results,
#   as soon as they're available.
# - Exception handling - if one of the tasks raises an exception we won't be able
#   to process the remaining tasks.
# For those reasons we should use asyncio convenience helpers.
# - asyncio.gather() - concurrently runs a sequence of awaitables.
#   If given a coroutine, wraps it in a task for us.
#   .gather() guarantees that results are returned in the same order they were passed in,
#   despite the inherent indeterminism.


# We may want to use a for loop or list comprehension to create multiple tasks.
# However we must avoid some pitfalls here - awaiting immediately, probably
# isn't what we want here - it results in synchronous code.
@async_timed()
async def create_tasks_bad() -> None:
    delay_times = (2, 2, 2)
    [await asyncio.create_task(delay(seconds)) for seconds in delay_times]


# Instead we should create the tasks first and only await them
# once all the work has been scheduled and started.
@async_timed()
async def create_tasks_better() -> None:
    delay_times = (2, 2, 2)
    tasks = [asyncio.create_task(delay(seconds)) for seconds in delay_times]
    [await task for task in tasks]


# Even better, use asyncio.gather() to correctly handle exceptions, etc.
@async_timed()
async def create_tasks_gather() -> None:
    delay_times = (3, 2, 1)
    delays = [delay(seconds) for seconds in delay_times]
    tasks = asyncio.gather(*delays)
    results = await tasks
    # .gather() guarantees that the results will be [3, 2, 1]
    print(results)

async def main():
    await create_tasks_bad()
    print()
    await create_tasks_better()
    print()
    await create_tasks_gather()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectoEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
