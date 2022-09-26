#!/usr/bin/env python3

import asyncio
import socket

from keyword import kwlist

MAX_KEYWORD_LEN = 4



# The `await` keyword works with `awaitables`.
# As an end user of asyncio the most common awaitables will be:
# * native coroutine objects, obtained from calling native coroutine functions
# * asyncio.Task, usually obtained from passing a coroutine object to asyncio.create_task()
# Lower level awaitables:
# * objects with an __await__ method - e.g. asyncio.Future
# * Objects written in other languages using Python/C API with `tp_as_async.am_await` funrction
#   returning an iterator (symilar to __await__).
#
# If we don't intend to keep track of a coroutine or manage it (e.g. .cancel() it)
# there's no need to hold on to the reference to asyncio.Task, just creating the task
# with asyncio.create_task() is enough to start it.


# Return a domain name and a boolean indicating if it resolved (i.e. it exists).
async def probe(domain: str) -> tuple[str, bool]:
    # Get a reference to the asyncio event loop.
    # Prefer .get_running_loop() over .get_event_loop() - the latter is deprecated.
    loop = asyncio.get_running_loop()
    try:
        # loop.getaddrinfo() coroutine-method - retuns a five-part tuple parameter,
        # to connect to the given address using a socket. Here we ignore the result,
        # we only care if an exception was raised - if it was the domain doesn't
        # exist, otherwise it does.
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return (domain, False)
    return (domain, True)


# main() must be a coroutine, so that we can use await here.
async def main() -> None:
    names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
    # Generator yielding domain names wtih .dev suffix
    domains = (f'{name}.dev'.lower() for name in names)
    # Build a list of coroutine objects by invoking the probe coroutine with each domain argument.
    coros = [probe(domain) for domain in domains]
    # asyncio.as_completed - generator yielding coroutines that return
    # the result of the coroutines passed to it in the order they are completed.
    # This is similar to futures.as_completed().
    for coro in asyncio.as_completed(coros):
        # .as_completed returns done coroutines, however we still need to use
        # `await` here to get the result. Any potential exceptions will be re-raised here.
        domain, found = await coro
        mark = '+' if found else ' '
        print(f'{mark} {domain}')


if __name__ == '__main__':
    asyncio.run(main()) # starts the event loop and returns only when the event loop exits.
