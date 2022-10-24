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
from asyncio import StreamReader


# asyncio can offer non-blocking commandline input.
# This can be done using the StreamReader in conjunction with StreamReaderProtocol class,
# which can be used to connect sys.stdin to the StreamReader.
# All this is done with the help of `asyncio.connect_read_pipe` coroutine.


# Create a StreamReader capable of asynchronously reading the standard input.
async def create_stdin_reader() -> StreamReader:
    stream_reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream_reader)
    loop = asyncio.get_running_loop()
    # Connect the stream reader protocol to sys.stdin. The returned transport and protocol are ignored,
    # since we don't need them here (we already have a handle to the protocol).
    transport, protocol_ = await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream_reader


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
