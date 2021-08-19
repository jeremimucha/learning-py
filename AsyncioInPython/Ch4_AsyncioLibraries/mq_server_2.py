#! /usr/bin/env python
import asyncio
import argparse
from asyncio import StreamReader, StreamWriter, Queue
from collections import deque, defaultdict
from contextlib import suppress
from typing import Deque, DefaultDict, Dict
from msgproto import read_msg, send_msg

# This MQ implementation further decouples message sending,
# by introducing a channel queue. Not only is there a queue
# dedicated to each client, but there's also a queue dedicated
# to each channel/topic. The message data is pushed to the channel queue,
# rather than directly to each channel subscriber, thus further reducing
# the time the main client coro is busy sending messages.

SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)
SEND_QUEUES: DefaultDict[StreamWriter, Queue] = defaultdict(Queue)
CHAN_QUEUES: Dict[bytes, Queue] = {}


async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info("peername")
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    send_task = asyncio.create_task(send_client(writer, SEND_QUEUES[writer]))
    print(f"Remote {peername} subscribed to {subscribe_chan}")
    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            if channel_name not in CHAN_QUEUES:
                CHAN_QUEUES[channel_name] = Queue(maxsize=10)
                asyncio.create_task(chan_sender(channel_name))
            await CHAN_QUEUES[channel_name].put(data)
    except asyncio.CancelledError:
        print(f"Remote {peername} connection cancelled.")
    except asyncio.IncompleteReadError:
        print(f"Remote {peername} disconnected.")
    finally:
        print(f"Remote {peername} closed.")
        await SEND_QUEUES[writer].put(None)
        await send_task
        del SEND_QUEUES[writer]
        SUBSCRIBERS[subscribe_chan].remove(writer)


async def send_client(writer: StreamWriter, queue: Queue):
    while True:
        try:
            data = await queue.get()
        except asyncio.CancelledError:
            continue

        if not data:
            break
            
        try:
            await send_msg(writer, data)
        except asyncio.CancelledError:
            await send_msg(writer, data)

    writer.close()
    await writer.wait_closed()


async def chan_sender(name: bytes):
    with suppress(asyncio.CancelledError):
        while True:
            writers = SUBSCRIBERS[name]
            # Somewhat ugly - sleep for a while if there's no
            # channel subscribers. Note that the queue dedicated
            # to this channel will keep buffering the messages, so if there
            # are no readers it will overflow eventually.
            if not writers:
                await asyncio.sleep(1)
                continue
            if name.startswith(b'/queue'):
                writers.rotate()
                writers = writers[0:1]
            # Pushing None to the queue indicates request to shutdown the coro.
            if (msg := await CHAN_QUEUES[name].get()) is None:
                break
            for writer in writers:
                if not SEND_QUEUES[writer].full():
                    print(f"Sending to {name}: {msg[:19]}...")
                    await SEND_QUEUES[writer].put(msg)
                else:
                    print(f"Dropped message '{msg[:19]}' to {name}. Buffer full.")


async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument('--host', default='127.0.0.1')
    argp.add_argument('--port', default=25000, type=int)
    args = argp.parse_args()
    try:
        asyncio.run(main(client, host=args.host, port=args.port))
    except KeyboardInterrupt:
        print("Shutting down...")
