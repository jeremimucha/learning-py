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
from asyncio import StreamReader, StreamWriter
import uvloop


# Asyncio makes it possible to inject a different implementation of the event loop.
# It's possible to implement our own - by subclassing AbstractEventLoop, but
# there are opensource alternatives available already.
#
# One commonly used event loop is `uvloop`, which is built on top of `libuv` library
# implemented in C - it's the backbone of node.js.
# `uvloop` performs really well in socket and stream-based applications.


async def connected(reader: StreamReader, writer: StreamWriter):
    line = await reader.readline()
    writer.write(line)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(connected, port=9000)
    await server.serve_forever()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Use uvloop as the event loop - this needs to be done before calling asyncio.run(main())
    uvloop.install()

    # The above is equivalent to
    # loop = uvloop.new_event_loop()
    # asyncio.set_event_loop(loop)

    asyncio.run(main())
 