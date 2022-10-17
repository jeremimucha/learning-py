#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
print(_ROOT)
sys.path.append(str(_ROOT))

import asyncio

from util.delay_functions import delay


async def add_one(number: int) -> int:
    return number + 1


async def hello_world() -> str:
    # await asyncio.sleep(1)
    await delay(1)
    return 'Hello World!'


async def main() -> None:
    # await pauses the current coroutine and won't execute any other code
    # inside that coroutine until the await expression give us the value.
    # This means we can not actually achieve any concurrency this way.
    # To actually run concurrently we need `tasks`.
    message = await hello_world()   # pause main until hello_world returns
    a = await add_one(1)            # pause main until add_one returns
    print(a)
    print(message)


if __name__ == '__main__':
    asyncio.run(main())
