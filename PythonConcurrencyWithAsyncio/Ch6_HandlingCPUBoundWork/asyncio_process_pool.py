#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List


def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter += 1
    return counter


async def main():
    with ProcessPoolExecutor() as process_pool:
        loop: AbstractEventLoop = asyncio.get_running_loop()
        nums = [1, 3, 5, 22, 100000000]
        # Create partially applied functions for countdown with arguments.
        # This is necessary, because ProcessPoolExecutor accepts only callables
        # that can be called with no arguments.
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []
        # Submit each call to the process pool and append it to a list.
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))

        # Wait for all results to finish
        results = await asyncio.gather(*call_coros)

        for result in results:
            print(result)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
