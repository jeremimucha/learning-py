#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))


import socket
from Ch14_AdvancedAsyncio.custom_event_loop.custom_task import CustomTask
from Ch14_AdvancedAsyncio.custom_event_loop.custom_event_loop import EventLoop


# Read data from cthe client, and log it.
async def read_from_client(conn, loop: EventLoop):
    print(f'Reading data from client {conn}')
    try:
        while data := await loop.sock_recv(conn):
            print(f'Got {data} from client!')
    finally:
        loop.sock_close(conn)

# Listen for client connections, creating a task to read data when a client connects.
async def listen_for_connections(sock, loop: EventLoop):
    while True:
        print('Waiting for connection...')
        conn, addr = await loop.sock_accept(sock)
        CustomTask(read_from_client(conn, loop), loop)
        print(f'I got a new connection from {sock}!')


async def main(loop: EventLoop):
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(('127.0.0.1', 8000))
    server_socket.listen()
    server_socket.setblocking(False)

    await listen_for_connections(server_socket, loop)


if __name__ == '__main__':
    event_loop = EventLoop()
    event_loop.run(main(event_loop))
