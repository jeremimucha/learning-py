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

from util import async_timed, fetch_status


@async_timed()
async def gather_requests():
    async with aiohttp.ClientSession() as session:
        # urls = ['https://example.com' for _ in range(1000)]
        # If you don't want to spam some remote service with requests start a local server (see local_server)
        urls = ['http://127.0.0.1:8000' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        # Uncomment to compare how long sequential code would take.
        # status_codes = [await request for request in requests]
        print(status_codes)


# By default .gather re-raises exceptions thrown by the tasks it executes.
# However, even though one (or more) of the coroutines failed, remaining coroutines
# are not canceled and will continue to run as long as we handle the exception,
# or the exception does not result in the event loop being stopped.
# - This may be considered a drawback of gather() - we might want to cancel other tasks instead.
# - Another issue is that we will see only the first exception thrown, if multiple tasks fail.
# - For those reasons it is recommended to use `return_exceptions=True` by default.
@async_timed()
async def default_handling_exceptions():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        requests = [fetch_status(session, url) for url in urls]
        status_codes = await asyncio.gather(*requests)
        print(status_codes)


@async_timed()
async def better_handling_exceptions():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com', 'python://example.com']
        requests = [fetch_status(session, url) for url in urls]
        results = await asyncio.gather(*requests, return_exceptions=True)

        exceptions = [res for res in results if isinstance(res, Exception)]
        successful_results = [res for res in results if not isinstance(res, Exception)]
        print(f'All results: {results}')
        print(f'Finished successfully: {successful_results}')
        print(f'Threw exceptions: {exceptions}')


@async_timed()
async def main():
    # await gather_requests()
    print()
    # await default_handling_exceptions()
    print()
    await better_handling_exceptions()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectoEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
