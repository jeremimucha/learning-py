#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import StreamReader, StreamWriter
import logging


# Simple Chat Server using asyncio and asyncio.Streams
#
# 1. A chat client should be able to connect to the server when they provide a username.
# 2. Once a user is connected, they should be able to send chat messages to the server,
#    and each message should be sent to every user connected to the server.
# 3. To pevernt idle users takin up resources, if a user is idle for more than one minute,
#    the server should disconnect them.


class ChatServer:

    def __init__(self):
        self._username_to_writer = {}

    async def start_chat_server(self, host: str, port: int):
        server = await asyncio.start_server(self.client_connected, host, port)

        async with server:
            await server.serve_forever()

    # Wait for the client to provide a valid username command; otherwise, disconnect them.
    async def client_connected(self, reader: StreamReader, writer: StreamWriter):
        command = await reader.readline()
        print(f'CONNECTED {reader} {writer}')
        command, args = command.split(b' ')
        if command == b'CONNECT':
            username = args.replace(b'\n', b'').decode()
            self._add_user(username, reader, writer)
            await self._on_connect(username, writer)
        else:
            logging.error('Got invalid command from client, disconnecting.')
            writer.close()
            await writer.wait_closed()

    # Store a user's stream writer instance and create a task to listen for messages.
    def _add_user(self, username: str, reader: StreamReader, writer: StreamWriter):
        self._username_to_writer[username] = writer
        asyncio.create_task(self._listen_for_messages(username, reader))

    async def _on_connect(self, username: str, writer: StreamWriter):
        writer.write(f'Welcome! {len(self._username_to_writer)} user(s) are online!\n'.encode())
        await writer.drain()
        await self._notify_all(f'{username} connected!\n')

    async def _remove_user(self, username: str):
        writer = self._username_to_writer[username]
        del self._username_to_writer[username]
        try:
            writer.close()
            await writer.wait_closed()
        except Exception as e:
            logging.exception('Error closing client writer, ignoring.', exc_info=e)
        
    # Listen for messages from a client and send them to all other clients,
    # waiting a maximum of a minute for a message.
    async def _listen_for_messages(self, username: str, reader: StreamReader):
        try:
            while (data := await asyncio.wait_for(reader.readline(), 60)) != b'':
                await self._notify_all(f'{username}: {data.decode()}')
            await self._notify_all(f'{username} has left the chat\n')
        except Exception as e:
            logging.exception('Error reading from client.', exc_info=e)
            await self._remove_user(username)

    # Send a message to all connected clients, removing any disconnected users.
    async def _notify_all(self, message: str):
        inactive_users = []
        for username, writer in self._username_to_writer.items():
            try:
                writer.write(message.encode())
                await writer.drain()
            except ConnectionError as e:
                logging.exception('Could not writer to client.', exc_info=e)
                inactive_users.append(username)

        [await self._remove_user(username) for username in inactive_users]


async def main():
    chat_server = ChatServer()
    await chat_server.start_chat_server('127.0.0.1', 8000)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
