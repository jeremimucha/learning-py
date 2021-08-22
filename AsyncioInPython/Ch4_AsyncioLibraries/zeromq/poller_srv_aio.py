#! /usr/bin/env python

# Program demonstratic asyncio-based poller service
import asyncio
import zmq
import itertools, time
from zmq.asyncio import Context
from contextlib import suppress


context = Context()

async def do_pusher():
    pusher = context.socket(zmq.PUSH)
    pusher.bind("tcp://*:5557")
    with suppress(asyncio.CancelledError):
        for i in itertools.count():
            await asyncio.sleep(1)
            await pusher.send_json(i)
            # print(f"PUSH sent {i}")
    pusher.close()


async def do_publisher():
    publisher = context.socket(zmq.PUB)
    publisher.bind("tcp://*:5556")
    with suppress(asyncio.CancelledError):
        for i in itertools.count():
            await asyncio.sleep(1)
            await publisher.send_json(i)
            # print(f"PUB sent {i}")
    publisher.close()


async def main():
    await asyncio.gather(
        do_pusher(),
        do_publisher(),
    )


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
        context.term()
