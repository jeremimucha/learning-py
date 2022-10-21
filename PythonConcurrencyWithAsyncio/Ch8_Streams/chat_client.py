#!/usr/bin/env python3

import logging
from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import StreamReader, StreamWriter
from collections import deque
import shutil
import tty
from typing import (
    Deque,
    Callable,
    Awaitable
)

from Ch8_Streams.stdin_reader import create_stdin_reader


# 1. When a user starts the application, the client should prompt for a username
#    and attempt to connect to the server.
# 2. Once connected, the user will see any messages from other clients scroll down
#    from the top of the screen.
# 3. The user should have an input field at the bottom of the screen.
#    When the user presses Enter, the text in the input should be sent to the server
#    and then to all other connected clients.

def save_cursor_position():
    sys.stdout.write('\0337')

def restore_cursor_position():
    sys.stdout.write('\0338')

def move_to_top_of_screen():
    sys.stdout.write('\033[H')

def delete_line():
    sys.stdout.write('\033[2K')

def clear_line():
    sys.stdout.write('\033[2K\033[0G')

def move_back_one_char():
    sys.stdout.write('\033[1D')

def move_to_bottom_of_screen() -> int:
    _, total_rows = shutil.get_terminal_size()
    input_row = total_rows - 1
    sys.stdout.write(f'\033[{input_row}E')
    # sys.stdout.flush()
    return total_rows


async def read_line(stdin_reader: StreamReader) -> str:
    # Convenience function to delete the previous character from standard output
    def erase_last_char():
        move_back_one_char()
        sys.stdout.write(' ')
        move_back_one_char()

    backspace_char = b'\x7f'
    enter_char = b'\n'
    input_buffer = deque()
    while (input_char := await stdin_reader.read(1)) != enter_char:
        # If the input character is backspace, remove the last char
        if input_char == backspace_char:
            if len(input_buffer) > 0:
                input_buffer.pop()
                erase_last_char()
                sys.stdout.flush()
        else:
            # If the input char is not backspace, append it to the buffer and echo
            input_buffer.append(input_char)
            sys.stdout.write(input_char.decode())
    clear_line()
    return b''.join(input_buffer).decode()


class MessageStore:
    def __init__(self, callback: Callable[[Deque], Awaitable[None]], max_size: int):
        self._deque = deque(maxlen=max_size)
        self._callback = callback

    async def append(self, item):
        self._deque.append(item)
        await self._callback(self._deque)


async def send_message(message: str, writer: StreamWriter):
    writer.write((message + '\n').encode())
    await writer.drain()

# Listen for messages from the server, appending them to the message store.
async def listen_for_messages(reader: StreamReader, message_store: MessageStore):
    while (message := await reader.readline()) != b'':
        await message_store.append(message.decode())
    await message_store.append('Server closed connection.')


# Read input from the user, and send it to the server.
async def read_and_send(stdin_reader: StreamReader, writer: StreamWriter):
    while True:
        message = await read_line(stdin_reader)
        await send_message(message, writer)


async def main():
    async def redraw_output(items: deque):
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            sys.stdout.write(item)
        restore_cursor_position()

    tty.setcbreak(0)
    os.system('clear')
    rows = move_to_bottom_of_screen()

    messages = MessageStore(redraw_output, rows - 1)

    stdin_reader = await create_stdin_reader()
    sys.stdout.write('Enter username: ')
    sys.stdout.flush()
    username = await read_line(stdin_reader)

    # Open a connection to the server, and send the connect message with the username.
    reader, writer = await asyncio.open_connection('127.0.0.1', 8000)

    writer.write(f'CONNECT {username}\n'.encode())
    await writer.drain()

    message_listener = asyncio.create_task(listen_for_messages(reader, messages))
    input_listener = asyncio.create_task(read_and_send(stdin_reader, writer))

    try:
        done, pending = await asyncio.wait([message_listener, input_listener], return_when=asyncio.FIRST_COMPLETED)    
    except Exception as e:
        logging.exception(e)
        writer.close()
        await writer.wait_closed()

    for done_task in done:
        if done_task.exception() is None:
            writer.write(done_task.result())
        else:
            writer.write(f'Request got an exception {done_task.exception()}')
    
    # Here we cancel pending tasks.
    for pending_task in pending:
        pending_task.cancel()



if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
