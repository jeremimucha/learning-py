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
    fetch_status,
    async_timed
)


# asyncio.as_completed() allows us to handle results of awaitables as they become avaialble.
# It takes a list of awaitables and returns an iterable of Futures. We can then iterate
# over the futures, awaiting each one. When the await expression completes, we will
# retrieve the result of the coroutine >>that finished first out of all our awaitables<<.
# This means we can process results as soon as they're available.
# We loose the ordering of the awaitables - there's no guarantee which request completes first.

@async_timed()
async def using_as_completed():
    async with ClientSession() as session:
        # fetchers = [fetch_status(session, 'https://www.example.com', 1),
        #             fetch_status(session, 'https://www.example.com', 1),
        #             fetch_status(session, 'https://www.example.com', 10),]
        fetchers = [fetch_status(session, 'http://localhost:8000', 1),
                    fetch_status(session, 'http://localhost:8000', 1),
                    fetch_status(session, 'http://localhost:8000', 10),
                    fetch_status(session, 'http://localhost:8000'),
                    fetch_status(session, 'http://localhost:8000'),
                    fetch_status(session, 'http://localhost:8000'),]

        for finished_task in asyncio.as_completed(fetchers):
            print(await finished_task) # Any potential exceptions will be thrown here


# We can set a timeout on an entire group of awaitables given to .as_completed().
# All the awaitables after the timeout expires will throw TimeoutError.
@async_timed()
async def as_completed_with_timeout():
    async with ClientSession() as session:
        # fetchers = [fetch_status(session, 'https://www.example.com', 1),
        #             fetch_status(session, 'https://www.example.com', 1),
        #             fetch_status(session, 'https://www.example.com', 10),]
        fetchers = [fetch_status(session, 'http://localhost:8000', 1),
                    fetch_status(session, 'http://localhost:8000', 1),
                    fetch_status(session, 'http://localhost:8000', 10),
                    fetch_status(session, 'http://localhost:8000', 10),
                    fetch_status(session, 'http://localhost:8000'),
                    fetch_status(session, 'http://localhost:8000'),]
        
        for done_task in asyncio.as_completed(fetchers, timeout=2):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print('We got a timeout error!')


async def main():
    await using_as_completed()
    print()
    await as_completed_with_timeout()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
