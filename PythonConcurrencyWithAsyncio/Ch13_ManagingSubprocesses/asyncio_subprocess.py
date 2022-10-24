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


async def main():
    if os.name == 'nt':  # Windows
        process: Process = await asyncio.create_subprocess_exec('cmd', '/c', 'dir')
    else:
        process: Process = await asyncio.create_subprocess_exec('ls', '-l')
    
    print(f'Process pid is: {process.pid}')
    status_code = await process.wait()
    print(f'Status code: {status_code}')


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
