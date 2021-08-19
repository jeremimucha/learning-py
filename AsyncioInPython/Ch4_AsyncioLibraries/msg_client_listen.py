#! /usr/bin/env python
import asyncio
import argparse, uuid
from msgproto import read_msg, send_msg


# An MQ client that only listens on a channel/topic.
# It will send a subscribtion message and only read incomming messages
# from that point on.


async def main(host, port, channel):
    me = uuid.uuid4().hex[:8]   # create a listener id
    # Start a connection with the server
    print(f"Starting up {me}")
    reader, writer = await asyncio.open_connection(host, port)
    print(f'I am {writer.get_extra_info("sockname")}')
    # Encode the given channel to bytes and send a message
    # to the server, indicating that this is the channel
    # we'd like to subscribe to.
    channel = channel.encode()
    await send_msg(writer, channel)
    try:
        while data := await read_msg(reader):
            print(f"Received by {me}: {data[:20]}")
        print("Connection ended.")
    except asyncio.IncompleteReadError:
        print("Server closed.")
    finally:
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument("--host", default='localhost')
    argp.add_argument("--port", default=25000)
    argp.add_argument("--channel", default='/topic/foo')
    args = argp.parse_args()
    try:
        asyncio.run(main(args.host, args.port, args.channel))
    except KeyboardInterrupt:
        print("Shutting down...")
