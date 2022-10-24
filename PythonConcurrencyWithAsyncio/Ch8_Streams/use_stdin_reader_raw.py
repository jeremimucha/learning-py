#!/usr/bin/env python3

from pathlib import Path
import sys
import os
from termios import CREAD
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

# Set terminal into raw mode, that still handles CTRL-C and other special keys for us.
import tty  # For setcbreak()

import asyncio
from asyncio import StreamReader
from collections import deque
import shutil   # for get_terminal_size
from typing import Callable, Deque, Awaitable

from Ch8_Streams.stdin_reader import create_stdin_reader
from util import delay


# Using the terminal in `cbreak` mode requires us to handle buffering what the user types,
# and echoing the input. If the stream operated in pure `raw` mode, we'd also need to handle
# all the special keys like CTRL-C.
#
# 1. The user input field should always remain at the bottom of the screen,
# 2. Coroutine output should start from the top of the screen and move down,
# 3. When there are more message than available lines on the screen, existing messages
#    should scroll up.

# 1. Move the cursor to the bottom of the screen and when key a is pressed, append it to our internal buffer,
#    and echo the keypress to standard out.
# 2. When the user presses Enter, create a delay task. Instead of writing output messages to standard out,
#    we'll append them to a deque with a maximum number of elements equal to the number of rows on the consol
# 3. Once a message goes into the deque, we'll redraw the output on the screen. We first move the cursor
#    to the top left of the screen. We then print out all messages in the deque. Once we're done,
#    we return the cursor to the input row and column where it was before.

# Moving the cursor around the screen - using ANSI escape codes.
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
# - escape sequence prefix -> `\033`
# - control sequence introducers are started by printing `\033[`

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
            sys.stdout.flush()
    clear_line()
    return b''.join(input_buffer).decode()


class MessageStore:
    def __init__(self, callback: Callable[[Deque], Awaitable[None]], max_size: int):
        self._deque = deque(maxlen=max_size)
        self._callback = callback

    async def append(self, item):
        self._deque.append(item)
        await self._callback(self._deque)


# Append the output messages to the MessageStore and sleep for the given amount of time.
async def sleep(delay: int, message_store: MessageStore):
        await message_store.append(f'Starting delay {delay}')
        await asyncio.sleep(delay)
        await message_store.append(f'Finished delay {delay}')


async def main():
    tty.setcbreak(sys.stdin)
    os.system('clear')
    rows = move_to_bottom_of_screen()

    # Callback to move the cursor to the top of the screen; redraw output and move the cursor back
    async def redraw_output(items: deque):
        save_cursor_position()
        move_to_top_of_screen()
        for item in items:
            delete_line()
            print(item)
        restore_cursor_position()

    messages = MessageStore(redraw_output, rows - 1)
    stdin_reader = await create_stdin_reader()

    while True:
        line = await read_line(stdin_reader)
        delay_time = int(line)
        asyncio.create_task(sleep(delay_time, messages))


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
