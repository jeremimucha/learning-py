#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio.subprocess import Process


# Asyncio can start and manage subprocesses for us (since the subprocess module is blocking).
# This is done with:
# * create_subprocess_exec
# * create_subprocess_shell - use this only if some of the shell functionality is needed


async def simple_subprocess():
    if os.name == 'nt':  # Windows
        # Looks like asyncio.subprocess actually isn't implemented on Windows yet,
        # this throws NotImplemented exception.
        process: Process = await asyncio.create_subprocess_exec('cmd', '/c', 'dir')
    else:
        process: Process = await asyncio.create_subprocess_exec('ls', '-l')
    
    print(f'Process pid is: {process.pid}')
    status_code = await process.wait()
    print(f'Status code: {status_code}')

    # If we wanted to use .wait_for() in the above example to introduce a timeout,
    # the thing to be aware of is that only the coroutine will be canceled,
    # not the underlying process!
    # Instead it's necessary to call .terminate() or .kill() which send the
    # SIGTERM or SIGKILL signals respectively.


async def terminating_subprocesses():
    process: Process = await asyncio.create_subprocess_exec('sleep', '3')
    print(f'Process pid is: {process.pid}')
    try:
        status_code = await asyncio.wait_for(process.wait(), timeout=1.0)
        print(status_code)
    except asyncio.TimeoutError:
        print('Timed out waiting to finish,terminating...')
        process.terminate()
        # Wait for the process to finish after sending the signal.
        # Note that this still can take a long time, so .wait_for() might make sense here.
        # Maybe wrapped in another try-catch and sending .kill() if .terminate() wasn't enough.
        status_code = await process.wait()
        print(status_code)

async def main():
    await simple_subprocess()
    await terminating_subprocesses()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
