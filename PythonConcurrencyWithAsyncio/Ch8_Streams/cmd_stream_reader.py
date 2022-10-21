#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio


# asyncio can offer non-blocking commandline input.
# This can be done using the StreamReader in conjunction with StreamReaderProtocol class,
# which can be used to connect sys.stdin to the StreamReader.
# All this is done with the help of `asyncio.connect_read_pipe` coroutine.


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
