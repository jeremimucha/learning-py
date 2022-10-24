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
from asyncio import Semaphore, BoundedSemaphore


# Bounded Semaphores should be used in situations where a semaphore is managed manually,
# which introduces a risk it it will be released more times than it was acquired.
# A regular Semaphore would be in a corrupted state after such operation,
# but the Bounded Semaphore willinstead raise the `ValueError` exception.

async def acquire(semaphore: Semaphore):
    print('Waiting to acquire')
    async with semaphore:
        print('Acquired')
        await asyncio.sleep(5)
    print('Releasing')


async def release(semaphore: Semaphore):
    print('Releasing as a one off!')
    semaphore.release()
    print('Released as a one off!')


async def main():
    # Normal Semaphore will not detect this missuse.
    # Instead, if it is released too many times, its limit will increase
    semaphore = Semaphore(2)
    
    print('Acquiring twice, releasing three times...')
    await asyncio.gather(acquire(semaphore),
                         acquire(semaphore),
                         release(semaphore))
    
    # Because we release once too many times, the following call will actually succeed.
    print("Acquiring three times...")
    await asyncio.gather(acquire(semaphore),
                         acquire(semaphore),
                         acquire(semaphore),)

    # Instead we should use the BoundedSemaphore, which will catch this error:
    # The following will raise ValueError("BoundedSemaphore released too many times.")
    bounded_sem = BoundedSemaphore()
    await asyncio.gather(acquire(bounded_sem),
                        acquire(bounded_sem),
                        release(bounded_sem))


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
