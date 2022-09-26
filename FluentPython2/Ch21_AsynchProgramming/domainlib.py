import asyncio
import socket
from collections.abc import Iterable, AsyncIterator
from typing import NamedTuple, Optional


# Use NamedTuple to make the result easier to read and debug.
class Result(NamedTuple):
    domain: str
    found: bool


# Convenience type alias
OptionalLoop = Optional[asyncio.AbstractEventLoop]


# `probe` gets an optional `loop` argument, to avoid repeated
# calls to asyncio.get_running_loop() when this coroutine
# is driven by multi_probe.
async def probe(domain: str, loop: OptionalLoop = None) -> Result:
    if loop is None:
        loop = asyncio.get_running_loop()
    try:
        await loop.getaddrinfo(domain, None)
    except socket.gaierror:
        return Result(domain, False)
    return Result(domain, True)

# An asynchronous generator function produces an asynchronous generator object,
# which can be annotated as AsyncIterator[SomeType]
async def multi_probe(domains: Iterable[str]) -> AsyncIterator[Result]:
    loop = asyncio.get_running_loop()
    # Build a list of probe coroutine ojbects, each with a different domain,
    coros = [probe(domain, loop) for domain in domains]
    # This is not an `async for` because as_completed() is a classic generator.
    for coro in asyncio.as_completed(coros):
        # Await on the coroutine object to retrieve the result.
        result = await coro
        # Yield the result. This line makes `multi_probe` an asynchronous generator.
        yield result
        # The above two lines could be written as
        # yield await coro
        # Precedence rules make this
        # yield (await coro)
