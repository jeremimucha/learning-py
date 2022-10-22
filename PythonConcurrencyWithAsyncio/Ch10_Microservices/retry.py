#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import logging
from typing import Callable, Awaitable


class TooManyRetries(Exception):
    pass


async def retry(coro: Callable[[], Awaitable],
                max_retries: int,
                timeout: float,
                retry_interval: float):
    for retry_num in range(0, max_retries):
        try:
            # Wait for a response for the specified timeout.
            return await asyncio.wait_for(coro(), timeout=timeout)
        except Exception as e:
            logging.exception(f'Exception while waiting (tried {retry_num} times), retrying.', exc_info=e)
            await asyncio.sleep(retry_interval)
        # If we failed to many times, raise an exception to indicate that.
    raise TooManyRetries()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    async def main():
        async def always_fail():
            raise Exception("I've failed!")

        async def always_timeout():
            await asyncio.sleep(1)

        try:
            await retry(always_fail, max_retries=3, timeout=.1, retry_interval=.1)
        except  TooManyRetries:
            print('Retries too many times!')
        
        try:
            await retry(always_timeout, max_retries=3, timeout=.1, retry_interval=.1)
        except TooManyRetries:
            print('Retries too many times!')
    
    asyncio.run(main())
