#!/usr/bin/env python3

import asyncio
import time
from contextlib import asynccontextmanager


# Defining async context managers using contextlib.asynccontextmanager


def download_webpage(url: str) -> str:
    print("Downloading a website")
    time.sleep(1)
    return f'Foobar-{url}'


def update_stats(url: str) -> None:
    print(f'Updating status of website: {url}')
    time.sleep(1)


def process(data: str) -> None:
    print(f'Processing: {data}')

# The decorated function must be an asynchronous generator.
@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_running_loop()
    # Suppose `download_webpage` is some blocking function here.
    # We run it in a separate thread to avoid blocking the event loop.
    data = await loop.run_in_executor(None, download_webpage, url)
    # All lines before this yield expression become the `__aenter__`
    # coroutine method of the asyncrhonous context manager built by the decorator.
    yield data
    # Lines after the `yield` become the `__aexit__` coroutine method.
    # Here, another blocking call is delegated to the thread executor.
    await loop.run_in_executor(None, update_stats, url)


async def supervisor():
    # Use `web_page` with `async with`.
    async with web_page('google.com') as data:
        process(data)


if __name__ == '__main__':
    asyncio.run(supervisor())
