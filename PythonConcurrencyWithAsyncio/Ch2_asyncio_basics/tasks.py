#!/usr/bin/env python3

from pathlib import Path
import sys
from unittest import result
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import CancelledError

from util import delay

# Tasks are wrappers around coroutines that schedule a coroutine to run on the event loop as soon as possible.
# This scheduling and execution happen in a non-blocking fashion, meaning that once we create a task,
# we can execute other code instantly, while the task is running.
# This is one way to achieve concurrency with coroutines.

async def sleep_once():
    sleep_for_three = asyncio.create_task(delay(3))
    print(type(sleep_for_three))
    print('Doing other stuff...')
    result = await sleep_for_three
    print(result)


async def sleep_thrice():
    sleep1 = asyncio.create_task(delay(3))
    sleep2 = asyncio.create_task(delay(3))
    sleep3 = asyncio.create_task(delay(3))

    await sleep1
    await sleep2
    await sleep3


async def hello_every_second():
    for _ in range(3):
        await asyncio.sleep(1)
        print("I'm running other code while I'm waiting!")

async def sleep_with_message():
    sleep1 = asyncio.create_task(delay(3))
    sleep2 = asyncio.create_task(delay(3))
    await hello_every_second()
    await sleep1
    await sleep2


# Cancelling tasks, waiting with a timeout

async def cancelling_tasks():
    long_task = asyncio.create_task(delay(10))

    seconds_elapsed = 0
    while not long_task.done():
        print('Task not finished, checking again in a second.')
        await asyncio.sleep(1)
        seconds_elapsed += 1
        if seconds_elapsed == 5:
            # Calling .cancel() on a task causes it to raise `CancelledError`.
            # This will only happen when the coroutine reaches the next await
            # statement in the task (coroutine) - i.e. a suspention point.
            long_task.cancel()

    try:
        await long_task
    except CancelledError:
        print('Our task was cancelled')


async def await_with_timeout():
    delay_task = asyncio.create_task(delay(2))
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Got a timeout!')
        print(f'Was the task cancelled? {delay_task.cancelled()}')   # True


# Ignoring cancellation requests:

# Sometimes we may want to monitor long running tasks, but instead of cancelling it entirely,
# we might want to perform some additional actions if it is taking too long, but still have
# the ability to continue execution.
# This is what `asyncio.shield` allows - it will intercept the cancel request,
# and return the task in a state that can be further awaited.
async def shield_cancellation():
    task = asyncio.create_task(delay(10))

    try:
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print("Task took longer than five seconds, it will finish soon!")
        result = await task # we can still await to resume the execution and let it finish.
        print(result)


async def main() -> None:
    await sleep_once()
    print("")
    await sleep_thrice()
    print("")
    await sleep_with_message()
    print("")
    await cancelling_tasks()
    print("")
    await await_with_timeout()
    print("")
    await shield_cancellation()
    print("")

if __name__ == '__main__':
    asyncio.run(main())
