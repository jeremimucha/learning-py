#! /usr/bin/env python
import asyncio
import argparse, uuid
from itertools import count
from msgproto import send_msg


async def main(host, port, channel, interval, size):
    me = uuid.uuid4().hex[:8]
    print(f"Starting up {me}")
    reader, writer = await asyncio.open_connection(host=args.host, port=args.port)
    print(f'I am {writer.get_extra_info("sockname")}')

    # sender doesn't listen for any messages, it strictly sends them,
    # indicate this by subscribing to a '/null' channel - expect
    # no clients to try to write to this channel.
    # The server could implement logic to simply ignore all
    # messages written to the '/null' channel.
    listen_channel = b'/null'
    await send_msg(writer, listen_channel)

    chan = channel.encode()
    try:
        for i in count():
            await asyncio.sleep(interval)
            data = b'X'*size or f'Msg {i} from {me}'.encode()
            try:
                await send_msg(writer, chan)
                await send_msg(writer, data)
            except OSError:
                print("Server closed the connection.")
                break
    except asyncio.CancelledError:
        writer.close()
        await writer.wait_closed()


if __name__ == '__main__':
    argp = argparse.ArgumentParser()
    argp.add_argument("--host", default="localhost")
    argp.add_argument("--port", default=25000, type=int)
    argp.add_argument("--channel", default='/topic/foo')
    argp.add_argument("--interval", default=1, type=float)
    argp.add_argument("--size", default=0, type=int)

    args = argp.parse_args()
    try:
        asyncio.run(main(args.host, args.port, args.channel, args.interval, args.size))
    except KeyboardInterrupt:
        print("Shutting down...")
