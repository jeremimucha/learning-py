#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Condition
from contextlib import suppress


# Conditions are a combination of Lock and Event. They're used as follows:
# Initially the condition's lock is acquired, giving us access to the shared state.
# Then we wait for a specific event to occur using .wait() or .wait_for(),
# these coroutines release the lock, and block until the event happens,
# afterwards again acquiring the lock. (Much like std::condition_variable).


async def do_work(id:int, condition: Condition):
    while True:
        print(f'Worker {id}: Waiting for condition lock...')
        # Wait to acquire the condition lock
        async with condition:
            print(f'Worker {id}: Acquired lock, releasing and waiting for condition...')
            # Release the lock and wait for an event to occur, which re-acquires the lock.
            await condition.wait()
            print(f'Worker {id}: Condition event fired, re-acquiring lock and doing work...')
            await asyncio.sleep(1)
            # Once we exit the async with block, release the condition lock.
            print(f'Worker {id}: Work finished, lock released.')

async def fire_event(condition: Condition):
    while True:
        await asyncio.sleep(5)
        print('About to notify, acquiring condition lock...')
        async with condition:
            print('Lock acquired, notifying all workers.')
            # Notify all tasks that the event has happened
            condition.notify_all()
        print('Notification finished, releasing lock.')

async def simple_condition_demo():
    condition = Condition()

    events_task = asyncio.wait_for(asyncio.create_task(fire_event(condition)), 20)
    with suppress(asyncio.TimeoutError):
        await asyncio.gather(asyncio.wait_for(do_work(1, condition), 20),
                            asyncio.wait_for(do_work(2, condition), 20),
                            events_task)


async def main():
    await simple_condition_demo()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
