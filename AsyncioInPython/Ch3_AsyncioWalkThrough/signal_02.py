#! /usr/bin/env python
import asyncio
from signal import SIGINT, SIGTERM

# Example demonstrates how to handle both SIGINT/SIGTERM
# and perform clean shutdown, while also doing cleanup
# in the CancelledError coro termination case.


async def main():
    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        # pretend we're doing long-running cleanup
        for _ in range(3):
            print('<Your app is shutting down...>')
            await asyncio.sleep(1)


def handler(sig):
    loop = asyncio.get_running_loop()
    # This is only valid if we're not relying on
    # asyncio.run - otherwise we'll get errors,
    # that a loop was terminated before tasks were finished.
    loop.stop()
    print(f"Got signal: {sig!s}, shutting down.")
    # Stop handling signals - the shutdown/cleanup procedure
    # is ongoing - avoid interrupting it.
    loop.remove_signal_handler(SIGTERM)
    # Removing the SIGINT handler would result in
    # the default SIGINT handler taking over - the default
    # handler throws KeyboardInterrupt exception.
    # Instead register a do-nothing handler for SIGINT.
    loop.add_signal_handler(SIGINT, lambda: print("<Got SIGINT; Ignoring>"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)
    loop.create_task(main())
    loop.run_forever()
    # cleaup
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()
