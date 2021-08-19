#! /usr/bin/env python

# Extremely simple fire-and-forget tcp echo server example
# from the asyncio docs: https://docs.python.org/3/library/asyncio-stream.html

import asyncio


async def handle_echo(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    data = await reader.read(100)   # read 100 bytes
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"[Server] Received {message!r} from {addr!r}")

    print(f"[Server] Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print(f"[Server] Closing the connection: {addr!r}")
    writer.close()


async def main():
    server = await asyncio.start_server(handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f"[Server] Serving on {addr}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("[Server] Shutting down...")
