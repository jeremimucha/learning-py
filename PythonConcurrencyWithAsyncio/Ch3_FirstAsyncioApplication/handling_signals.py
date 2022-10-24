#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import asyncio
from asyncio import (
    AbstractEventLoop,
)
import signal
from typing import Set

from util import delay


def cancel_tasks():
    print('Got a SIGINT')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f'Cancelling {len(tasks)} task(s).')
    [task.cancel() for task in tasks]


async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)

    await delay(10)


if __name__ == '__main__':
    asyncio.run(main())
