#! /usr/bin/env python
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor as Executor


# Example demonstrates that running computation in an executor doesn't guarantee
# clean cooperative shutdown with coroutines (executor runs Futures).
# This is true for python 3.8, python 3.9 apparently handles this case.
# For python 3.8 - the unfinished Future will raise an exception.

async def main():
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, blocking)
    print(f"{time.ctime()} Hello")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")


# The blocking function sleeps longer than the main coroutine.
def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")


# pre-python 3.9 this will result in the executor Future returned for `blocking`
# raising an exception.
# try:
#     asyncio.run(main())
# except KeyboardInterrupt:
#     print("Bye!")

# ------------------------------------------------------------------------------------------------
# 1. Possible solution to this issue is to always explicitly await the Future returned
#    by the executor.

async def main_1():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking)
    try:
        print(f"{time.ctime()} Hello!")
        await asyncio.sleep(1.0)
        print(f"{time.ctime()} Goodbye!")
    finally:
        # Explicitly await the Future (futures?) which we're running on an executor.
        # This works but is verbose.
        await future

# This would correctly wait for the Future started in the main_1 coro.
# try:
#     asyncio.run(main_1())
# except KeyboardInterrupt:
#     print("Bye!")


# ------------------------------------------------------------------------------------------------
# 2. Another solution is to rely on the fact that asyncio.run will wait for all Tasks.
#    We can be sneaky and wrap the Future returned by run_in_executor in a task.

# This is a rather clumsy/sneaky option - we need to wrap every Future in a coro explicitly
# and register a task with the loop.
async def make_coro(future):
    try:
        return await future
    except asyncio.CancelledError:
        return await future


async def main_2():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking)
    asyncio.create_task(make_coro(future))
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")

# This would also ensure proper shutdown
# try:
#     asyncio.run(main_2())
# except KeyboardInterrupt:
#     print("Bye!")


# ------------------------------------------------------------------------------------------------
# 3. Another option would be to abandon the asyncio.run loop and write our own

async def main_3():
    loop = asyncio.get_running_loop()
    print(f"{time.ctime()} Hello!")
    await asyncio.sleep(1.0)
    print(f"{time.ctime()} Goodbye!")
    loop.stop()

# custom loop
loop = asyncio.get_event_loop()
executor = Executor()
loop.set_default_executor(executor)
loop.create_task(main_3())
future = loop.run_in_executor(None, blocking)
try:
    loop.run_forever()
except KeyboardInterrupt:
    print("Cancelled")

tasks = asyncio.all_tasks(loop=loop)
for t in tasks:
    t.cancel()
group = asyncio.gather(*tasks, return_exceptions=True)
loop.run_until_complete(group)
executor.shutdown(wait=True)
loop.close()
