#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import aiohttp
from aiohttp import ClientSession

from util import (
    fetch_status,
    async_timed
)


# For finer-grained control use `.wait()` instead of .gather() or .as_completed().
# It allows us to explicitly control the tasks, e.g. cancelling the remaining ones,
# if one fails, and it allows us to be explicit about the order we await the tasks in.
# .wait() accepts:
#   - list of awaitables (in the future it will accept only Task objects)
#   - optional `return_when` string
# return_when:
#   - ALL_COMPLETED
#   - FIRST_EXCEPTION
#   - FIRST_COMPLETED


@async_timed()
async def using_wait():
    async with ClientSession() as session:
        # fetchers = \
        #     [asyncio.create_task(fetch_status(session, 'https://example.com')),
        #      asyncio.create_task(fetch_status(session, 'https://example.com')),]
        fetchers = \
            [asyncio.create_task(fetch_status(session, 'http://localhost:8000')),
             asyncio.create_task(fetch_status(session, 'http://localhost:8000')),]

        done, pending = await asyncio.wait(fetchers)    # default: ALL_COMPLETED
    
        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        # The done tasks still need to be awaited to retrieve the result.
        # Any potential exceptions will be rethrown at this point.
        # Alternatively we could use the task.result() and task.exception() methods here,
        # instead of awaiting.
        for done_task in done:
            result = await done_task
            print(result)


@async_timed()
async def wait_handle_exceptions():
    async with ClientSession() as session:
        # good_request = fetch_status(session, 'https://example.com')
        good_request = fetch_status(session, 'http://localhost:8000')
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [asyncio.create_task(good_request),
                    asyncio.create_task(bad_request),]

        done, pending = await asyncio.wait(fetchers)

        print(f'Done task count: {len(done)}')
        print(f'Pending task cound: {len(pending)}')

        for done_task in done:
            # result = await done_task # will throw an exception
            if done_task.exception() is None:
                print(done_task.result())
            else:
                print(f"Request got an exception: {done_task.exception()}")


# We might want to react to any exceptions thrown by our awaitables immediately.
# This can be done by using the FIRST_EXCEPTION `return_when` policy.
# With this policy, .wait() will return as soon as a first exception is thrown.
# This gives us two possible outcomes
# - No exceptions were thrown - this is then equivalent to ALL_COMPLETED policy.
# - One or more exceptions were thrown.
#   The done set is then guaranteed to contain at least one task failed with an exception.
#   It might also contain more failed tasks as well as successfully completed tasks.
@async_timed()
async def wait_handle_first_exception():
    async with ClientSession() as session:
        # good_request_1 = fetch_status(session, 'https://example.com', delay=3)
        # good_request_2 = fetch_status(session, 'https://example.com', delay=3)
        good_request_1 = fetch_status(session, 'http://localhost:8000', delay=3)
        good_request_2 = fetch_status(session, 'http://localhost:8000', delay=3)
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [asyncio.create_task(bad_request),
                    asyncio.create_task(good_request_1),
                    asyncio.create_task(good_request_2),
                    ]

        done, pending = await asyncio.wait(fetchers, return_when=asyncio.FIRST_EXCEPTION)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            if done_task.exception() is None:
                print(done_task.result())
            else:
                print(f'Request got an exception {done_task.exception()}')
        
        # Here we cancel pending tasks, we could handle these however we need, e.g. schedule them again.
        for pending_task in pending:
            pending_task.cancel()


# FIRST_COMPLETED - let's us handle results as they become available, much like .as_completed()
# If we need this behavior, but can't use .as_completed() because we also want to be able to
# tell which tasks have completed and which are remaining we can use this policy with .wait().
# 
# .wait() with FIRST_COMPLETED behaves as follows:
# - returns as soon as it has at least one result - either successful or failed one.
@async_timed()
async def wait_handle_first_completed():
    async with ClientSession() as session:
        # url = 'https://www.example.com'
        url = 'http://localhost:8000'
        pending = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url)),]

        # Loop until there are pending tasks
        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)

            print(f'Done task count: {len(done)}')
            print(f'Pending task count: {len(pending)}')

            # We could also handle exceptions here and cancel all pending tasks
            for done_task in done:
                print(await done_task)


# TIMEOUTS - .wait() also allows us to handle timeouts.
# - When timeouts occur coroutines are not cancelled.
#   We must explicitly loop over the tasks and cancel them if we so desire.
# - No TimeoutErrors are raised - instead if a timeout occurs, .wait()
#   returns all tasks that are `done` and all `pending` up to that point.
@async_timed()
async def wait_handle_timeout():
    async with ClientSession() as session:
        # url = 'https://www.example.com'
        url = 'http://localhost:8000'
        fetchers = [asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url)),
                    asyncio.create_task(fetch_status(session, url, delay=5)),]

        # The tasks that timeout will be returned in the `pending` set
        done, pending = await asyncio.wait(fetchers, timeout=3)

        print(f'Done task count: {len(done)}')
        print(f'Pending task count: {len(pending)}')

        for done_task in done:
            result = await done_task
            print(result)

        # Note that the pending tasks are still running, despite the timeout.
        # If that's our use case, we need to cancel them explicitly.
        # for pending_task in pending:
        #     pending_task.cancel()


async def main():
    # await using_wait()
    # print()
    # await wait_handle_exceptions()
    # print()
    # await wait_handle_first_exception()
    # print()
    # await wait_handle_first_completed()
    # print()
    await wait_handle_timeout()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectoEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
