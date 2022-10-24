#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import asyncio
import functools
import selectors
from selectors import BaseSelector
import socket

from Ch14_AdvancedAsyncio.custom_event_loop.custom_future import CustomFuture


# Set the connection socket on the future when a client connects.
def accept_connection(future: CustomFuture, connection: socket):
    print(f'We got a connection from {connection}!')
    future.set_result(connection)


# Register the accept_connection function with the selector
# and pause to wait for a client connection.
async def sock_accept(sel: BaseSelector, sock) -> socket:
    print('Registering socket to listen for connections')
    future = CustomFuture()
    sel.register(sock, selectors.EVENT_READ, functools.partial(accept_connection, future))
    print('Pausing to listen for connections...')
    connection: socket = await future
    return connection


async def main(sel: BaseSelector):
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('127.0.0.1', 8000))
    sock.listen()
    sock.setblocking(False)

    # Wait for a client to connect
    print('Waiting for socket connection!')
    connection = await sock_accept(sel, sock)
    print(f'Got a connection {connection}')


# Loop forever, calling send on the main coroutine.
# Each time a selector event occurs, run the register callback.
def loop():
    selector = selectors.DefaultSelector()
    coro = main(selector)

    # Minimal viable event loop.
    # Creates an instance of the main coroutine function,
    # calls .send(None) to advance to the first await/yield.
    # selector.select than blocks until a client is connected,
    # after which we handle all the registered callbacks - accept_connection in this case.
    # Calling .send(None) again progresses beyond all the await calls and terminates the application.
    while True:
        try:
            state = coro.send(None)

            # Calling selector.select blocks until a client connects.
            events = selector.select()

            # Calls any registered callbacks.
            # In our case this will be the `accept_connection` function.
            for key, mask in events:
                print('Processing selector events...')
                callback = key.data
                callback(key.fileobj)
        except StopIteration as si:
            print('Application finished!')
            break



if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop()
