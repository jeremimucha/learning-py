#! /usr/bin/env python

import asyncio

# Async context managers are useful whenever it's necessary to await someting
# inside the enter/exit methods of a context manager.


# Pretend to establish a connection
async def get_conn(host, port):
    await asyncio.sleep(1.0)
    print(f"Establishing connection {host}:{port}")
    return Connection(host, port)


# The Connection class is an async context manager.
# It implements __aenter__ and __aexit__ coroutines, which manage the
# context asynchronously.
class Connection:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def close(self):
        await asyncio.sleep(0.1)
        print(f"Closing the connection {self.host}:{self.port}")
    
    # async equivalent of the __enter__ method
    async def __aenter__(self):
        self.conn = await get_conn(self.host, self.port)
        print(f"Creating context")
        return self.conn

    # async equivalent of the __exit__ method
    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()
        print("Closing context")


# Just as any other async object async context managers can only by used
# within the context of a coroutine (i.e. inside the body of an `async def` function).
async def use_async_context():
    async with Connection('localhost', 9001) as conn:
            pass



# ------------------------------------------------------------------------------------------------
# The contextlib way.
#
# The same can be achieved, much like with non-async context managers using contextlib,
# which now exposes an @asynccontextmanager decorator.
# Note that this approach requires that all objects used internally by the contextmanager
# need to be themselves coroutines (awaitable).
from contextlib import asynccontextmanager


# context 'enter' coroutine
async def download_webpage(url):
    print("Requesting the webpage: ", url)
    await asyncio.sleep(0.5)
    return """<!DOCTYPE html>
<html>
  <head>
    <title>Dummy page</title>
  </head>
  <body>
    <p>Hello async</p>
  </body>
</html>"""


# context 'exit' coroutine
visit_stats = dict()
async def update_status(url):
    print("Updating visit_stats...")
    await asyncio.sleep(0.1)
    cur = visit_stats.get(url, 0)
    visit_stats[url] = cur + 1


@asynccontextmanager
async def web_page(url):
    # Note that both download_webpage and update_status need to be awaitable
    data = await download_webpage(url)
    # Using yield in an `async def` function makes this an
    # asynchronous generator function.
    try:
        yield data  # everything after the yield is the `__aexit__` part of the context manager
    except Exception:
        print("Exception thrown within the context.")
    finally:
        await update_status(url)


async def use_async_web_page():
    async with web_page("https://foobar.com") as data:
        print(data)
    print("visit_stats: ", visit_stats)


# ------------------------------------------------------------------------------------------------
# Wrapping blocking calls, when used with contextmanagers.
# If we don't have access to the functions we'd like to use within the contextmanager
# we can always wrap the blocking calls into Futures using the asyncio.run_in_executor
import time

def blocking_download_webpage(url):
    time.sleep(0.5)
    print("Requesting the webpage: ", url)
    return """<!DOCTYPE html>
<html>
  <head>
    <title>Dummy page</title>
  </head>
  <body>
    <p>Hello async</p>
  </body>
</html>"""

blocking_visit_stats = {}
def blocking_update_status(url):
    print("Updating blocking_visit_stats...")
    time.sleep(0.1)
    cur = blocking_visit_stats.get(url, 0)
    blocking_visit_stats[url] = cur + 1


@asynccontextmanager
async def web_page_2(url):
    # To get around the blocking calls we access the event loop
    # and run the calls via an executor.
    #
    # loop = asyncio.get_event_loop()
    # Preffer the following:
    loop = asyncio.get_running_loop()
    # Note that everything should be wrapped in a try-except as usual with context managers.
    data = await loop.run_in_executor(None, blocking_download_webpage, url)
    yield data 
    await loop.run_in_executor(None, blocking_update_status, url)


async def use_async_web_page_2():
    async with web_page_2("https://foobar.com") as data:
        print(data)
    print("blocking_visit_stats: ", blocking_visit_stats)


if __name__ == '__main__':

    asyncio.run(use_async_context())
    
    # ------------------------------------------------------------------------------------------------
    print("\nUsing a context manager defined with @asynccontextmanager")
    asyncio.run(use_async_web_page())
    # ------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------
    print("\nUsing an async context manager with blocking calls delegated to executor:")
    asyncio.run(use_async_web_page_2())
    # ------------------------------------------------------------------------------------------------
