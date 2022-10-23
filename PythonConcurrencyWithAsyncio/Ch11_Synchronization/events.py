#!/usr/bin/env python3

import functools
from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Event
from contextlib import suppress


# asyncio Events can be used to wait until some arbitrary condition that the Event represents occur.
# All the coroutines waiting for the Event will block until the Event is .set().
# After it is set, further calls to .wait() will no longer block, until the event is .clear()'ed.

# Note however that Events can be missed by workes. If a long running coroutine is doing work,
# while an event occurs, but another worked clears the event in the mean time,
# the first worker will never react to that event.


def trigger_event(event: Event):
    event.set()

async def do_work_on_event(event: Event):
    print('Waiting for event...')
    # Blocks until an event occurs.
    await event.wait()
    # Once the event occurs, wait no longer blocks and we can do the work.
    print('Performing work!')
    await asyncio.sleep(1)
    print('Finished work!')
    # Reset the event, so future calls to wait will block.
    event.clear()

async def simple_event_demo():
    event = asyncio.Event()
    # Trigger the event 5 seconds in the future
    asyncio.get_running_loop().call_later(5.0, functools.partial(trigger_event, event))
    # Do some work that depends on event
    await asyncio.gather(do_work_on_event(event), do_work_on_event(event))


# Show how events can be missed.
# Workers will miss some events occuring, due to being busy doing work.
# If it's unacceptable to miss events, it's better (necessary) to use a Queue (AsyncQueue).

async def trigger_event_periodically(event: Event):
    while True:
        print('Triggering event!')
        event.set()
        await asyncio.sleep(1)

async def do_work_on_event(id: int, event: Event):
    while True:
        print(f'[{id}] Waiting for event...')
        await event.wait()
        event.clear()
        print(f'[{id}] Performing work!')
        # Some workers may miss an event occuring, due to the long running work here.
        await asyncio.sleep(5)
        print(f'[{id}] Finished work!')

async def missed_events_demo():
    event = asyncio.Event()
    # Keep triggering the event every 1 second for 5 seconds.
    trigger = asyncio.wait_for(trigger_event_periodically(event), 5.0)

    with suppress(asyncio.TimeoutError): # suppress is a context manager that ignores the given exception(s)
        await asyncio.gather(do_work_on_event(1, event), do_work_on_event(2, event), trigger)


async def main():
    # await simple_event_demo()
    await missed_events_demo()

if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
