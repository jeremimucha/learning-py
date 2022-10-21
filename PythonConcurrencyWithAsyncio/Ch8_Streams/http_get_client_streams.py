#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import StreamReader
from typing import AsyncGenerator


# Streams
# - open_connection - coroutine taking a host and port to connect to and creating a StreamReader and StreamWriter.
# - readline - coroutine taht waits until we have a line of data.
# - StreamReader.read - coroutine that waits for a specified number of bytes.
# - StreamWriter.write - plain method - implementation tries to write to the underlying socket immediately,
#   if the socket's buffer is full, the data is buffered internally (non-blocking).
# - StreamWriter.drain - coroutine waiting until a the write buffer is sent


async def read_until_empty(stream_reader: StreamReader) -> AsyncGenerator[str, None]:
    # Read a line and decode it until we don't have any left.
    while response := await stream_reader.readline():
        yield response.decode()


async def make_request():
    host: str = 'www.example.com'
    request: str = f'GET / HTTP/1.1\r\n' \
                   f'CONNECTION: close\r\n' \
                   f'Host: {host}\r\n\r\n'

    stream_reader, stream_writer = await asyncio.open_connection(host, 80)

    try:
        # Write the http request, and drain the writer.
        stream_writer.write(request.encode())
        await stream_writer.drain()

        # Read each line and store it in a list
        responses = [response async for response in read_until_empty(stream_reader)]

        print(''.join(responses))
    finally:
        # Close the writer and wait for it to finish closing.
        # Waiting until the connection is actually closed is considered best practice,
        # assuming we're concerned with any potential issues (exceptions) that might
        # occur while closing.
        stream_writer.close()
        await stream_writer.wait_closed()


async def main():
    await make_request()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
