#! /usr/bin/env python

# The "Janus" queue can be used to communicate between threads and coroutines
# in a non-blocking way. It exposes both a blocking and a non-blocking side of the api.
# The async side is of course meant to be used in coros, and the blocking on threads.

import asyncio
import random
import time
import janus


async def main():
    loop = asyncio.get_running_loop()
    queue = janus.Queue()
    # Run the threaded/blocking code in an executor
    future = loop.run_in_executor(None, data_source, queue)
    try:
        # In coro we use the asynchronous side of the queue interface.
        while (data := await queue.async_q.get()) is not None:
            print(f"Got {data} off queue")
        print("Done")
    finally:
        await future


def data_source(queue: janus.Queue):
    # The non-async side of the queue running in a thread
    # uses the blocking/synchronous interface of the queue.
    for i in range(10):
        r = random.randint(0, 4)
        time.sleep(r)   # blocking
        queue.sync_q.put(r)
    queue.sync_q.put(None)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopping...")
