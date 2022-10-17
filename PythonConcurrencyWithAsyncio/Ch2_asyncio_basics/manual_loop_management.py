#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio

from util import delay


def call_later():
    print("I'm being called in the future!")


async def main():
    # The event loop can be accessed explicitly in any function or coroutine.
    # Prefer asyncio.get_running_loop() instead of asyncio.get_event_loop().
    # The latter will start a loop if one isn't already running, which was shown to lead to bugs.
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)


if __name__ == '__main__':
    # This shows the basics of creating and running a loop explicitly.
    # This is similar to what happens when calling asyncio.run(),
    # what is missing is cancellation of any remaining tasks.
    loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(main())
    finally:
        loop.close()

    # asyncio.run() has an optional `debug` parameter. Set it to True,
    # To help with debugging event loop and coroutine issues.
    # It will print log messages when a coroutine or task takes more than 100 milliseconds to run.
    # The "slow task" time can be controlled with .slow_callback_duration member of the loop:
    #   loop = asyncio.get_event_loop()
    #   loop.slow_callback_duration = .250
    #
    #   asyncio.run(main(), debug=True)
    #
    # Debug mode can be enabled by passing a commandline argument when running python:
    #
    #   python3 -X dev program.py
    #
    # Or with an environment variable:
    #
    #   PYTHONASYNCIODEBUG=1 python3 program.py
