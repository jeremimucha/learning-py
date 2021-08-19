#! /usr/bin/env python

# Simple demo of a coroutine waiting until a socket receives data

import asyncio
import socket


async def wait_for_data():
    # Get a reference to the current event loop
    # to access low-level APIs.
    loop = asyncio.get_running_loop()

    # Create a pair of connected sockets.
    rsock, wsock = socket.socketpair()

    # Register the open socket to wait for data.
    reader, writer = await asyncio.open_connection(sock=rsock)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    data = await reader.read(100)

    # Got data, we are done: close the socket
    print("Received: ", data.decode())
    writer.close()

    # Close the second socket
    wsock.close()


if __name__ == '__main__':
    try:
        asyncio.run(wait_for_data())
    except KeyboardInterrupt:
        print("Shutting down.")
