#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import requests

from util import async_timed


@async_timed()
async def get_example_status() -> int:
    return requests.get('http://www.example.com').status_code

@async_timed()
async def get_many():
    # These tasks will not actually run concurrently, since the underlying api they call - requests,
    # is synchronous and blocking.
    # This can be avoided by either using an async library instead, like aiohttp,
    # or by delegating the blocking calls to a ThreadPool.
    task1 = asyncio.create_task(get_example_status())
    task2 = asyncio.create_task(get_example_status())
    task3 = asyncio.create_task(get_example_status())
    await task1
    await task2
    await task3


async def main() -> None:
    await get_many()


if __name__ == '__main__':
    asyncio.run(main())
