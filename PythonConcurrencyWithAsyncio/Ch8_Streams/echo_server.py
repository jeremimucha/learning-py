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
from asyncio import StreamReader, StreamWriter
import logging


# Creating servers with asyncio.
# Rather than using sockets, asyncio exposes `asymcio.start_server` coroutine.
# It accepts `host`, `port` and `client_connected_cb` (plus many more) parameters.
# The `client_connected_cb` is a function or a coroutine callback, that will run
# whenever a client connects to the server.
# This callback takes `StreamReader` and `StreamWriter` parameters, that let us
# read from and write to the client that connected to the server.
# .start_server returns AbstractServer object, which is a handle to the started server.
# It is also an async context manager.


class ServerState:

    def __init__(self):
        self._writers = []

    # Add a client to the server state, and create an echo task.
    async def add_client(self, reader: StreamReader, writer: StreamWriter):
        self._writers.append(writer)
        await self._on_connect(writer)
        asyncio.create_task(self._echo(reader, writer))

    # On a new connection, tell the client how many users are online, and notify others of a new user.
    async def _on_connect(self, writer: StreamWriter):
        writer.write(f'Welcome! {len(self._writers)} user(s) are online!\n'.encode())
        await writer.drain()
        await self._notify_all('New user connected!\n')

    # Handle echoing user input when a client disconnects, and notify other users of a disconnect.
    async def _echo(self, reader: StreamReader, writer: StreamWriter):
        try:
            while (data := await reader.readline()) != b'':
                writer.write(data)
                await writer.drain()
            self._writers.remove(writer)
            await self._notify_all(f'Client disconnected. {len(self._writers)} user(s) are online!\n')
        except Exception as e:
            logging.exception('Error reading from client.', exc_info=e)
            self._writers.remove(writer)

    # Helper method to send a message to all other users.
    # If a message fails to send remove that user.
    async def _notify_all(self, message: str):
        for writer in self._writers:
            try:
                writer.write(message.encode())
                await writer.drain()
            except ConnectionError as e:
                logging.exception('Could not write to client.', exc_info=e)
                self._writers.remove(writer)


async def main():
    server_state = ServerState()

    # When a client connects, add that client to the server state.
    async def client_connected(reader: StreamReader, writer: StreamWriter) -> None:
        await server_state.add_client(reader, writer)

    server = await asyncio.start_server(client_connected, '127.0.0.1', 8000)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
