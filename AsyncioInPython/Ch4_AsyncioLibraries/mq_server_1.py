#! /usr/bin/env python
import asyncio
import argparse
from asyncio import StreamReader, StreamWriter, Queue
from collections import deque, defaultdict
from contextlib import suppress
from typing import Deque, DefaultDict, Dict
from msgproto import read_msg, send_msg


# Improved implementation of the message queue.
# Deals with the main issue of the original design - the reading and sending
# is now decoupled using a Queue.
# Each client now has a dedicated Queue. The client coro reads messages
# and sends data to all clients subscribing on a particular topic, by
# pushing the data to the Queue. The `send_client` coro takes data
# off of the Queue and does the sending.


SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)
# Dedicated data Queue for each connected client
SEND_QUEUES: DefaultDict[StreamWriter, Queue] = defaultdict(Queue)


async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info("peername")
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    # Create the coro that handles message sending
    send_task = asyncio.create_task(send_client(writer, SEND_QUEUES[writer]))
    print(f"Remote {peername} subscribed to {subscribe_chan}")
    try:
        while channel_name := await read_msg(reader):
            data = await read_msg(reader)
            subs = SUBSCRIBERS[channel_name]
            if subs and channel_name.startswith(b'/queue'):
                subs.rotate()
                subs = subs[0:1]
            # Instead of sending messages directly in this coro
            # push the message data to respective client queues
            # this would block only if the Queue is full - we avoid this case
            # by explicitly dropping messages.
            for sub in subs:
                sub_queue = SEND_QUEUES[sub]
                if not sub_queue.full():
                    print(f"Sending to {channel_name}: {data[:19]}...")
                    await sub_queue.put(data)
                else:
                    print(f"Failed to send message '{data[:19]}' to {channel_name} - congested. Message dropped.")
    # Cleanup hasn't changed
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

        # Pushing None to the queue signals request to terminate the loop
        if data is None:
            break
            
        # Note that we send the message also
        # if the coro is cancelled - this is to ensure
        # all messages are pushed out before shutdown.
        try:
            await send_msg(writer, data)
        except asyncio.CancelledError:
            await send_msg(writer, data)

    writer.close()
    await writer.wait_closed()


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
