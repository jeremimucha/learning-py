#!/usr/bin/env python3
from pathlib import Path
import sys
import os
from typing import Any, Callable
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import functools
from concurrent.futures.thread import ThreadPoolExecutor
import hashlib
import os
import string
import time
import random

# In general Python Threading can not be used to improve performance of CPU-bound work.
# However, in some cases - whenever a module releases the GIL, while work is being done
# in low-level C code implementation, threading can be used to get the performance benefits.
# This requires that the code doesn't touch any python objects like dicts, lists, etc.
# A good example is python's `hashlib` library - which delegates all work to the
# underlying C implementation while releasing the GIL.
# This means we can use threads to get better performance.
# The same is true for some of the NumPy functionality
# (documentation isn't clearn on precisely what can benefit from multithreading through).


def random_password(length: int) -> bytes:
    ascii_lowercase = string.ascii_lowercase.encode()
    return b''.join(bytes(random.choice(ascii_lowercase)) for _ in range(length))


def hash(password: bytes) -> str:
    salt = os.urandom(16)
    return str(hashlib.scrypt(password, salt=salt, n=2048, p=1, r=8))


def single_threaded(passwords):

    print("Single threaded hashing started.")
    start = time.time()
    for password in passwords:
        hash(password)
    end = time.time()
    print(f"Single threaded total time: {end - start}")


async def multi_threaded(loop, passwords):
    tasks = []
    start = time.time()
    with ThreadPoolExecutor() as pool:
        for password in passwords:
            tasks.append(loop.run_in_executor(pool, functools.partial(hash, password)))

        await asyncio.gather(*tasks)
    end = time.time()
    print(f'Multi threaded total time: {end - start}')


async def main(passwords):
    loop = asyncio.get_running_loop()
    await multi_threaded(loop, passwords)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    passwords = [random_password(10) for _ in range(10000)]
    # single_threaded(passwords)

    asyncio.run(main(passwords))
