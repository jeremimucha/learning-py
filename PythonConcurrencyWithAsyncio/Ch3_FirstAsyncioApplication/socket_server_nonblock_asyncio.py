#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))


import asyncio
from asyncio import (
    AbstractEventLoop
)
import signal
import socket
from typing import Set

from util import delay


# Socket server implementation using asyncio.
# Utilizes low-level sockets, but schedules them on the asyncio event loop,
# using `sock_accept`, `sock_recv` and `sock_sendall`, analogous to the socket methods.

# 1. Accepting connections.
# - Uses sock_accept(server_socket)
# - We can only process one connectiona t a time, as socket.accept will only give us one client connection.
#   Behind the scenes, incomming connection will be stored in a `backlog` queue.
# - We don't need to process multiple connections concurrently - so this will be a simple loop,
#   accepting connections forever. This allows other code to run concurrently, while we're paused
#   waiting for a connection.
#
# 2. Reading and writing data from connected clients
# - We don't want to block other clients while we recv or send data from/to one of the clients.
#   Therefore a `task` will be used here, so that reading and writing can be done concurrently.
# - The task is created after `listen_for_connection` connects a client.
# - The client coroutine handles reading and writing forever, while that client is connected.
#
# Under the hood all of this uses selectors shown in `socket_server_nonblock_select.py`.


async def listen_for_connection(server_socket: socket.socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        # Whenever we get a connection, create an echo task, to listen for client data.
        asyncio.create_task(echo(connection, loop))


async def echo(connection: socket.socket, loop: AbstractEventLoop) -> None:
    # Loop forever waiting for data from a client connection.
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('Got data!')
            # Emulate exceptions while reading data.
            if data == b'boom\r\n':
                raise Exception("Unexpected network error")
            # Once we receive the data, send it back to the client.
            await loop.sock_sendall(connection, data)
    # Errors must be handled, either locally, as done here, or
    # the task must be `await`'ed somewhere, and the exception handled there.
    except Exception as ex:
        # logging.exception(ex)
        print(ex)
    # In either case we should take care to close the connection when we exit.
    finally:
        connection.close()


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    # Start the coroutine to listen for connections, thus starting the server
    await listen_for_connection(server_socket, asyncio.get_event_loop())

if __name__ == '__main__':
    asyncio.run(main())
