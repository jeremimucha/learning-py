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


# This example demonstrates a race condition that can occur in a networking application
# that sends messages to all users, when one of the users disconnects during the transmission,
# which triggers a callback that removes the user.


class MockSocket:
    def __init__(self):
        self.socket_closed = False

        # Simulate a slow send of a message to a client.
    async def send(self, msg: str):
        if self.socket_closed:
            raise Exception('Socket is closed!')
        print(f'Sending: {msg}')
        await asyncio.sleep(1)
        print(f'Sent: {msg}')

    def close(self):
        self.socket_closed = True


user_names_to_sockets = {'John': MockSocket(),
                         'Terry': MockSocket(),
                         'Graham': MockSocket(),
                         'Eric': MockSocket(),}

# Disconnect a user and remove them from application memory.
async def user_disconnect(username: str):
    print(f'{username} disconnected!')
    socket = user_names_to_sockets.pop(username)
    socket.close()


# Send messages to all users concurrently
async def message_all_users():
    print('Creating message tasks')
    messages = [socket.send(f'Hello {user}')
                for user, socket in
                user_names_to_sockets.items()
                ]
    # An exception will be thrown here, because the socket for one of the users will already be closed.
    await asyncio.gather(*messages)


async def main():
    await asyncio.gather(message_all_users(), user_disconnect('Eric'))


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
