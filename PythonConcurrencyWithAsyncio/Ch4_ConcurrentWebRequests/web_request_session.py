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
import aiohttp
from aiohttp import ClientSession
from util import async_timed


# aiohttp.ClientSession manages a session a session with recyclable connections,
# thus allowing for connection pooling, which cuts down on resource allocation costs,
# which in turn increases performance.


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as result:
        return result.status


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://example.com'
        status = await fetch_status(session, url)
        print(f'Status for {url} was {status}')


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid
    # `RuntimeError: Event loop is closed`.
    if os.name == 'nt':  # Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
