#!/usr/bin/env python3

"""Download flags of top 20 countries by population

asyncio + aiottp version

Sample run::

    $ python3 flags_asyncio.py
    EG VN IN TR RU ID US DE CN MX JP BD NG ET FR BR PH PK CD IR
    20 flags downloaded in 1.07s
"""
# tag::FLAGS_ASYNCIO_TOP[]
import asyncio

from httpx import AsyncClient

from flags import (
    # BASE_URL,
    save_flag,
    main
)

BASE_URL = 'http://localhost:8000/flags'

# Native coroutine - awaits on `get_flag()` which does the http request.
# Then it displays the code of the downloaded flag and saves the image.
async def download_one(client: AsyncClient, cc: str):
    image = await get_flag(client, cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc


async def get_flag(client: AsyncClient, cc: str) -> bytes:
    url = f'{BASE_URL}/{cc}/{cc}.gif'.lower()
    # AsyncClient.get() returns a ClientResponse object that is also an async context manager.
    resp = await client.get(url, timeout=6.1,
                                  follow_redirects=True)
    # Network I/O operations are implemented as coroutine methods,
    # so they are driven asynchronously by the asyncio event loop
    return resp.read()
# end::FLAGS_ASYNCIO_TOP[]


# Plain function - not a coroutine - so it canbe passed to and called by the main function
# from the flags.py module
def download_many(cc_list: list[str]) -> int:
    # Execute the event loop driving the supervisor(cc_list) coroutine object
    # until it returns.This will block while the event loop runs.
    # The result is whatever supervisor returns.
    return asyncio.run(supervisor(cc_list))

async def supervisor(cc_list: list[str]) -> int:
    # Asynchronous HTTP client operations in httpx are methods of AsyncClient,
    # which is also an asynchronous context manager - a context manager with
    # asynchronous setup and teardown methods
    async with AsyncClient() as client:
        # Build a list of coroutine objects by calling the download_one coroutine once
        # for each flag to be retrieved.
        to_do = [download_one(client, cc)
                 for cc in sorted(cc_list)]
        # asyncio.gather coroutine accepts one or more awaitable arguments,
        # and waits for all of them to complete, returning a list of results for the
        # given awaitables in the order they were submitted.
        res = await asyncio.gather(*to_do)

    # Return the length of the list returned by asyncio.gather
    return len(res)

if __name__ == '__main__':
    main(download_many)
# end::FLAGS_ASYNCIO_START[]
