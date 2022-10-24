#!/usr/bin/env python3

import functools
from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import asyncio
import time
import requests
from concurrent.futures import ThreadPoolExecutor

from util import async_timed


def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


# Run on a ThreadPool without using asyncio - we're just directly mapping the results using the pool.
def run_on_threadpool():
    start = time.time()
    # urls = ['https://www.example.com' for _ in range(1000)]
    urls = ['http://127.0.0.1:8000' for _ in range(1000)]
    with ThreadPoolExecutor() as pool:
        results = pool.map(get_status_code, urls)
        for result in results:
            print(result)

    end = time.time()

    print(f'Finished requests in {end - start:.4f} second(s)')


# Run on a ThreadPool using asyncio - schedule the tasks to .run_in_executor() and .gather() them.
# This doesn't really grant any performance benefits, but that's how ThreadPools are used with asyncio.
@async_timed()
async def asyncio_run_on_threadpool():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        # urls = ['https://www.example.com' for _ in range(1000)]
        urls = ['http://127.0.0.1:8000' for _ in range(1000)]
        tasks = [loop.run_in_executor(pool, functools.partial(get_status_code, url)) for url in urls]
        results = await asyncio.gather(*tasks)
        print(results)


# asyncio.run_in_executor() offers a default executor, if not passed in explicitly.
# The default executor is always a ThreadPoolExecutor, unless specified with `.set_default_executor()`
@async_timed()
async def asyncio_run_on_default_executor():
    loop = asyncio.get_running_loop()
    # urls = ['https://www.example.com' for _ in range(1000)]
    urls = ['http://127.0.0.1:8000' for _ in range(1000)]
    # asyncio will create and cache a default executor instance on first call to loop.run_in_executor(None, ...)
    # Every subsequent call reuses the default executor instance.
    tasks = [loop.run_in_executor(None, functools.partial(get_status_code, url)) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)


# Python3.9 introduced `asyncio.to_thread()` which simplifies scheduling work on the default thread pool further.
# It takes care of the partial application of arguments and the call to loop.run_in_executor for us.
@async_timed()
async def asyncio_run_to_thread():
    # urls = ['https://www.example.com' for _ in range(1000)]
    urls = ['http://127.0.0.1:8000' for _ in range(1000)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)


async def main():
    await asyncio_run_on_threadpool()
    await asyncio_run_on_default_executor()
    await asyncio_run_to_thread()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # run_on_threadpool()

    asyncio.run(main())
