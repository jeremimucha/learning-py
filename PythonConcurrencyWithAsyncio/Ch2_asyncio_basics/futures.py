#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Future


# Futures are objects that contain a single value, you expect to get at some point in the future.

def demo_future():
    f = Future()
    print(f'future.done()?: {f.done()}')

    f.set_result(42)    # Marks future as done.
    print(f'future.done()?: {f.done()}')

    result = f.result()
    print(f'Result of future: {result}')



# Awaiting futures - awaiting a future means that we suspend execution until the result of the future has been set.

async def set_future_value(future) -> None:
    await asyncio.sleep(1)  # wait before setting the value
    future.set_result(42)

def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_value(future))
    return future

async def awaiting_futures():
    future = make_request()
    print(f'Is the future done? {future.done()}')

    value = await future    # pause un til the future result is set
    print(f"Is the future done? {future.done()}")
    print(value)


async def main() -> None:
    await awaiting_futures()


if __name__ == '__main__':
    demo_future()
    print()

    asyncio.run(main())
