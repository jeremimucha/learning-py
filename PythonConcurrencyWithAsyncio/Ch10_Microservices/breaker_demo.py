#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from Ch10_Microservices.circuit_breaker import CircuitBreaker


async def main():
    async def slow_callback():
        await asyncio.sleep(2)

    cb = CircuitBreaker(slow_callback,
                        timeout=1.0,
                        time_window=5,
                        max_failures=2,
                        reset_interval=5)

    for _ in range(4):
        try:
            await cb.request()
        except Exception as e:
            pass

    print('Sleeping for 5 seconds so breaker closes...')
    await asyncio.sleep(5)
     
    for _ in range(4):
        try:
            await cb.request()
        except Exception as e:
            pass


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
