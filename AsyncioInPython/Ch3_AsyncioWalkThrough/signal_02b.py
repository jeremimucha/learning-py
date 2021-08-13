#! /usr/bin/env python
import asyncio
from signal import SIGINT, SIGTERM

# Example demonstrates how to handle signals and perform
# clean shutdown using the asyncio.run loop.
# All of the difficulty comes down to registering
# and unregistering the signal handlers correctly.
# The rest is done by asyncio.run.


async def main():
    loop = asyncio.get_running_loop()
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)
    
    try:
        while True:
            print("<Your app is running>")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        for i in range(3):
            print("<Your app is shutting down...>")
            await asyncio.sleep(1)


def handler(sig):
    # Initiate task cancellation.
    loop = asyncio.get_running_loop()
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()
    print(f"Got signal: {sig!s}, shutting down.")
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: print("<Got SIGINT; ignoring...>"))


if __name__ == '__main__':
    asyncio.run(main())
