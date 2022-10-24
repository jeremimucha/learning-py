#!/usr/bin/env python3

from pathlib import Path
import sys
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))


import asyncio
from asyncio import (
    AbstractEventLoop
)
import signal
import socket
from typing import List, Set

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
#
# 3. Graceful shutdown
# - Custom shutdown logic is added to allow in-progress tasks a few seconds to finish
#   sending messages they might want to send.
# - Uses signals and asyncio.all_tasks()
# - Unix-only (due to signals)
# - The overall idea is that we raise a custom exception when a signal is received,
#   we handle the exception and attempt to run all the active tasks to completion (with a timeout).
#
# This isn't really production-ready. A more robust implementation would also handle:
# - Stop accepting new incomming connections during shutdown - the connection listener
#   should be closed asap.
# - We only handle `TimeoutException`s in the shutdown handler, meaning that if anything else
#   was thrown, we'd capture that exception and any subsequent tasks that may have had an exception
#   will be ignored.

# We must maintain a list of all the tasks, so that we can gracefully close them.
echo_tasks = []


async def listen_for_connection(server_socket: socket.socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f"Got a connection from {address}")
        # Whenever we get a connection, create an echo task, to listen for client data.
        # Store the connection task on the list of tasks, so that we can gracefully
        # shut it down later.
        echo_task = asyncio.create_task(echo(connection, loop))
        echo_tasks.append(echo_task)


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


class GracefulExit(SystemExit):
    pass


def shutdown():
    raise GracefulExit()


async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            # We expect a timeout error here
            pass


async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()

    # Register signal handlers, so that we allow our connections some time to finish
    # processing any data.
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame), shutdown)

    # Start the coroutine to listen for connections, thus starting the server
    await listen_for_connection(server_socket, asyncio.get_event_loop())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, shutdown)

    try:
        loop.run_until_complete(main())
    except GracefulExit:
        loop.run_until_complete(close_echo_tasks(echo_tasks))
    finally:
        loop.close()
