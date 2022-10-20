#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from multiprocessing import Process, Value, Array


# It's possible to have data shared between processes.
# This will always be POD-style data, either plain Values or Arrays of plain Values.


def increment_value(shared_int: Value):
    # We need to synchronize the access if there are multiple producers/consumers
    # shared_int.get_lock().acquire()
    # shared_int.value += 1
    # shared_int.get_lock().release()

    # It's better to use a with block:
    with shared_int.get_lock():
        shared_int.value += 1


def increment_array(shared_array: Array):
    # We need to synchronize the access if there are multiple producers/consumers
    # shared_array.get_lock().acquire()
    # for index, integer in enumerate(shared_array):
    #     shared_array[index] = integer + 1
    # shared_array.get_lock().release()

    # Use a with block instead:
    with shared_array.get_lock():
        for index, integer in enumerate(shared_array):
            shared_array[index] = integer + 1



if __name__ == '__main__':
    # Issue on Windows - need to use the SelectoEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    integer = Value('i', 0)
    integer_array = Array('i', [0, 0])

    procs = [Process(target=increment_value, args=(integer,)),
             Process(target=increment_value, args=(integer,)),
             Process(target=increment_array, args=(integer_array,)),
             Process(target=increment_array, args=(integer_array,)),]
    
    [p.start() for p in procs]
    [p.join() for p in procs]

    print(integer.value)
    print(integer_array[:])
