#! /usr/bin/env python

import asyncio, time

# Using asyncio from an application developer standpoint can be simplified to the following steps:
# - Starting the asyncio event loop
# - Calling async/await functions
# - Creating a task to be run on the loop
# - Waiting for multiple tasks to complete
# - Closing the loop after all concurrent tasks have completed


async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 2:
        print("Usage: hello_asio.py [-raw]")
        print("  -raw - use raw event loop logic, rather then asyncio.run")
        sys.exit(1)
    
    raw = len(sys.argv) == 2 and sys.argv[1] == '-raw'

    if not raw:
        asyncio.run(main())
    else:
    # asyncio.run performs the equivalent of the following (not exactly, but close enough)
        print('Running raw event loop logic:')
        # Get a loop instance that will run all the coroutines.
        # If access to the loop inside of an `async def` function is necessary
        # the asyncio.get_running_loop() should be used.
        loop = asyncio.get_event_loop()
        # Create a task - it takes a coroutine - which is returned by an `async def` function.
        task = loop.create_task(main())
        # Run the even loop - this blocks the current thread while running all the scheduled tasks.
        loop.run_until_complete(task)
        # Once main thread is unblocked for any reason, we ensure that all pending tasks are finished
        # by canceling them and running until they're complete.
        pending = asyncio.all_tasks(loop=loop)
        for task in pending:
            task.cancel()
        group = asyncio.gather(*pending, return_exceptions=True)
        loop.run_until_complete(group)
        # Finally close the loop - it must be called on a stopped (completed) loop.
        loop.close()
