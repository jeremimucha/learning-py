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
from asyncio.subprocess import Process


async def show_deadlock():
    program = ['python3', 'deadlock_with_pipes_helper.py']
    process: Process = await asyncio.create_subprocess_exec(*program, stdout=asyncio.subprocess.PIPE)

    # If we run this example it will deadlock right after printing out the process pid.
    # What happens is that our stream reader buffer fills up, and any subsequent calls
    # to push more data onto it are blocking until more space becomes available.
    # The process is waiting still trying to finish writing to the buffer.
    # This is a circular dependency and therefore a deadlock.
    #
    # We would need to continuously drain the buffer so that more data can be written onto it.
    # An alternative is to avoid using .wait(), and instead use .communicate(), which avoids deadlocks
    # by consuming stdout and stderr.
    print(f'Process pid is: {process.pid}')
    return_code = await process.wait()
    print(f'Process returned: {return_code}')

async def communicate_no_deadlock():
    program = ['python3', 'deadlock_with_pipes_helper.py']
    process: Process = await asyncio.create_subprocess_exec(*program, stdout=asyncio.subprocess.PIPE)

    print(f'Process pid is: {process.pid}')

    # This will handle all stdout and stderr output automatically without deadlocks.
    # The downside is that we can't proces and react the output as the process runs
    # and maybe respond to stdin. To do that we need to manually manage using .wait as before.
    stdout, stderr = await process.communicate()
    print(stdout)
    print(stderr)
    print(f'Process returned: {process.returncode}')

async def main():
    # Uncomment to see the deadlock
    # await show_deadlock()

    await communicate_no_deadlock()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
