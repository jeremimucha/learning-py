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
from asyncio.subprocess import Process


# Keep reading as long as the stream isn't empty
async def write_output(prefix: str, stdout: StreamReader):
    while line := await stdout.readline():
        print(f'[{prefix}]: {line.rstrip().decode()}')


async def manage_subprocess_stdout():
    program = ['ls', '-la']
    process: Process = await asyncio.create_subprocess_exec(*program, stdout=asyncio.subprocess.PIPE)

    print(f'Process pid is: {process.pid}')
    stdout_task = asyncio.create_task(write_output(' '.join(program), process.stdout))

    return_code, _ = await asyncio.gather(process.wait(), stdout_task)
    print(f'Process returned: {return_code}')


async def main():
    await manage_subprocess_stdout()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
