#! /usr/bin/env python
import asyncio
from asyncio import StreamReader, StreamWriter, gather
from collections import deque, defaultdict
from typing import Deque, DefaultDict
from msgproto import read_msg, send_msg


# A smiplified message-queue ipc communication implemented based on Asyncio.
# The MQ supports topic-based messaging - all topic subscribers receive
# all messages broadcasted on the topic.


# Collection of active subscribers
# The first message a client sends is expected to be a channel name
# they wish to subscribe to.
#
# {channel -> list of subscribers}
SUBSCRIBERS: DefaultDict[bytes, Deque] = defaultdict(deque)


async def client(reader: StreamReader, writer: StreamWriter):
    peername = writer.get_extra_info('peername')
    # On connect -> expect a message with the channel the client subscribes to.
    subscribe_chan = await read_msg(reader)
    SUBSCRIBERS[subscribe_chan].append(writer)
    print(f"Remote {peername} subscribed to {subscribe_chan}")

    try:
        # Get the channel name to send the message to
        while channel_name := await read_msg(reader):
            # get the message itself
            data = await read_msg(reader)
            print(f"Sending to {channel_name}: {data[:19]}...")
            conns = SUBSCRIBERS[channel_name]
            # '/queue' is a magic keyword - it causes the message to
            # be sent to only one subscriber. The subscribers
            # are rotated in a queue-like fashin.
            if conns and channel_name.startswith(b'/queue'):
                conns.rotate()
                # conns = [conns[0]]
                conns = conns[0:1]
            # Send the data to all of the channel subscribers.
            # Note that this implementation is problematic -
            # it awaits ALL clients to be finished, essentially slowing
            # down the connection to the speed of the slowest subscriber.
            # The reading and writing of messages should be decoupled.
            await gather(*[send_msg(c, data) for c in conns])
    except asyncio.CancelledError:
        print(f"Remote {peername} closing connection.")
        writer.close()
        await writer.wait_closed()
    except asyncio.IncompleteReadError:
        print(f"Remote {peername} disconnected.")
    finally:
        print(f"Remote {peername} closed.")
        # Ensure we remove ourselves from the subscribers list
        # when we (the client) close the connection.
        SUBSCRIBERS[subscribe_chan].remove(writer)


async def main(*args, **kwargs):
    server = await asyncio.start_server(*args, **kwargs)
    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    try:
        asyncio.run(main(client, host='127.0.0.1', port=25000))
    except KeyboardInterrupt:
        print("Shutting down...")
