#! /usr/bin/env python

import asyncio

# Example of how to safeguard the main program loop against unhandled exceptions.
# This will ensure that all tasks run to completion, even if some of them throw.

async def foo(delay):
    await asyncio.sleep(1 / delay)  # delay == 0 will obviously throw
    return delay


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for i in range(10):
        loop.create_task(foo(i))
    # ensure smooth startup and shutdown
    pending = asyncio.all_tasks(loop)
    # return_exceptions will ensure that exceptions don't propagate
    # and terminate the program prematurely.
    group = asyncio.gather(*pending, return_exceptions=True)
    results = loop.run_until_complete(group)
    print(f'Results: {results}')
    # prints - "Results: [8, 3, 6, 1, 4, 9, 2, 7, ZeroDivisionError('division by zero'), 5]"
    loop.close()
