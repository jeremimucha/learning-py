#! /usr/bin/env python

# Extremely simple fire-and-forget tcp echo client example
# from the asyncio docs: https://docs.python.org/3/library/asyncio-stream.html
# - Sends a single message on localhost 8888.
# - Reads a message on the same port.
# - Closes the connection.

import asyncio


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    print(f'[Client] Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'[Client] Received: {data.decode()!r}')

    print('[Client] Closing the connection.')
    writer.close()


if __name__ == '__main__':
    try:
        asyncio.run(tcp_echo_client("Hello World!"))
    except KeyboardInterrupt:
        print('[Client] Shutting down.')
