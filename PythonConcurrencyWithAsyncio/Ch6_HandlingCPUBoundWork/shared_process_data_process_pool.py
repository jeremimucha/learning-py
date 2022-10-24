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
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Process, Value, Array


# ProcessPools introduce new challanges with sharing data.
# This is because of serialization/deserialization of the process arguments,
# we can not simply pass in the shared data as an argument - it's not serializable.
# Instead `process pool initializers` need to be used, to provide access to global
# shared process data.


# Shared process data. Note that it isn't initialized here
# but instead is initialized by the process pool initializer,
# handled by the process pool executor.
shared_counter: Value


# Process pool initializer.
# Initialization needs to be synchronized across all processes running in the process pool,
# since the script where the variable is declared will be ran by all the processess in the pool.
# Initializing it at the point of declaration would be a race condition.
def init(counter: Value):
    global shared_counter
    shared_counter = counter


def increment():
    with shared_counter.get_lock():
        shared_counter.value += 1


async def main():
    counter = Value('d', 0)
    loop = asyncio.get_running_loop()
    # Initialize the shared_counter for each process
    with ProcessPoolExecutor(initializer=init, initargs=(counter,)) as pool:
        tasks = [loop.run_in_executor(pool, increment) for _ in range(4)]
        await asyncio.gather(*tasks)
        print(counter.value)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectoEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
