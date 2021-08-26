#! /usr/bin/env python

# An app demonstrating the use of ZMQ to help with monitoring of a microservice-based
# application. The applications (microservices) are instrumented with asyncio/ZMQ
# based code to send metrics to a central microservice responsible for monitoring
# the state of other services.
#
# The central collection service receives all of the data from running services,
# and serves a webpage showing performance of other services in real time.

import argparse
import asyncio
import zmq, zmq.asyncio
import psutil
from random import (randint, uniform)
from datetime import (datetime as dt,
                      timezone as tz
                    )
from contextlib import suppress

LEAK_LIMIT = 100*1024*1024 # 100 MB

ctx = zmq.asyncio.Context()


# Instrumentation code - send data to the service collecting
# statistics about running services.
async def stats_reporter(color: str):
    p = psutil.Process()
    sock = ctx.socket(zmq.PUB)
    sock.setsockopt(zmq.LINGER, 1)
    sock.connect('tcp://localhost:5555')
    # Handler CancelledError by supperssing it
    with suppress(asyncio.CancelledError):
        while True:
            # ZMQ powers - serialize a dict and send it over the socket.
            await sock.send_json(dict(
                color=color,
                timestamp=dt.now(tz=tz.utc).isoformat(),
                cpu=p.cpu_percent(),
                mem=p.memory_full_info().rss / 1024 / 1024
            ))
            await asyncio.sleep(1)
    sock.close()


# The main microservice entrypoint
async def main(args):
    # Add the instrumentation
    asyncio.create_task(stats_reporter(args.color))
    leak = []
    with suppress(asyncio.CancelledError):
        while True: # main loop
            # fake work
            sum(range(randint(1_000, 10_000_000)))
            await asyncio.sleep(uniform(0, 1))
            # fake a memory leak
            leak += [0] * args.leak
            if leak > LEAK_LIMIT:
                leak.clear()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--color', type=str)
    parser.add_argument('--leak', type=int, default=0)
    args = parser.parse_args()
    try:
        asyncio.run(main(args))
    except KeyboardInterrupt:
        print('Shutting down...')
    finally:
        ctx.term()
