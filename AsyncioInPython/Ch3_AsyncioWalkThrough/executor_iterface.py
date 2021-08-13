#! /usr/bin/env python

import asyncio, time

# The executor interface allows us to run blocking functions (non-coroutines).
# This can be done either using the ThreadPoolExecutor or PorcessPoolExecutor.
# It is necessary to use this functionality when calling blocking functions.

async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


# Regular function definition (non-coroutine). Simulates a long-running computation.
# It can not be called directly in the same thread the event loop is running - it would
# cause it to stall.

def blocking():
    time.sleep(0.5)
    print(f'{time.ctime()} Hello from a thread!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())

    # Avoid blocking the event loop by running the `blocking` function in an executor (thread or process).
    # Executor begins only after `run_until_complete` is called.
    # It returns a Future object which can be await'ed e.g. if called from a coroutine.
    loop.run_in_executor(None, blocking) # The first arg is the executor instance, None means 'use default'.
    loop.run_until_complete(task)

    pending = asyncio.all_tasks(loop=loop)
    for task in pending:
        task.cancel()
    group = asyncio.gather(*pending, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
