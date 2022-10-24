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
from util import delay


# Asyncio's event loop can be forced to iterate by using a well-established and optimized idiom
# to suspend the current coroutine, forcing an iteration, calling `asyncio.sleep(0)`.


# Create two coroutine tasks and call gather.
# This behaves as expected - the coroutines don't actually start until the call to gather.
async def create_tasks_no_sleep():
    task1 = asyncio.create_task(delay(1))
    task2 = asyncio.create_task(delay(2))
    print('Gathering tasks:')
    await asyncio.gather(task1, task2)


# Create two coroutine tasks but interleave them with calls to asyncio.sleep(0).
# This causes the created tasks to start immediately, before the call to gather.
async def create_tasks_sleep():
    task1 = asyncio.create_task(delay(1))
    await asyncio.sleep(0)
    task2 = asyncio.create_task(delay(2))
    await asyncio.sleep(0)
    print('Gathering tasks:')
    await asyncio.gather(task1, task2)


async def main():
    print('--- Testing without asyncio.sleep(0) ---')
    await create_tasks_no_sleep()
    print('--- Testing with asyncio.sleep(0) ---')
    await create_tasks_sleep()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
