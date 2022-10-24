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
from asyncio import StreamWriter, StreamReader, Event
from asyncio.subprocess import Process



# This coro communicates with the spawned subprocess by sending some bytes into its stdin.
# Right after, the underlying process shuts down.
async def one_shot_stdin():
    program = ('python3', 'echo_user_input.py')
    process: Process = await asyncio.create_subprocess_exec(
        *program,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE
    )

    # Communicate waits until the process exits, so we'll get full output only after.
    # To read stdout and respond to stdin continuously we need to use process' exposed
    # StreamReader/StreamWriter objects.
    stdout, stderr = await process.communicate(b'Zoot')
    print(stdout) # This outputs b'Please enter a username: Your username is Zoot\n'
    print(stderr)

# ---

# If we need to continuously communicate between stdout/stdin we need to
# actively read the stdout of the process and write to stdin.
# This simple implementation has the downside that the reading and writing
# is strongly coupled.
async def consume_and_send(text_list, stdout: StreamReader, stdin: StreamWriter):
    for text in text_list:
        line = await stdout.read(2048)
        print(line)
        stdin.write(text.encode())
        await stdin.drain()

async def continuous_communication():
    program = ('python3', 'echo_user_while.py')
    process: Process = await asyncio.create_subprocess_exec(
        *program,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE
    )

    text_input = ['one\n', 'two\n', 'three\n', 'four\n', 'quit\n']

    await asyncio.gather(consume_and_send(text_input, process.stdout, process.stdin), process.wait())

# ---

# Decoupled reader and writer coroutines.
async def output_consumer(input_ready_event: Event, stdout: StreamReader):
    while (data := await stdout.read(1024)) != b'':
        print(data)
        # Only the reader coroutine now depends on the stdout of the process we're running:
        if data.decode().endswith("Enter text to echo: "):
            input_ready_event.set() # Set the event to trigger the writer coro.

async def input_writer(text_data, input_ready_event: Event, stdin: StreamWriter):
    for text in text_data:
        await input_ready_event.wait()
        stdin.write(text.encode())
        await stdin.drain()
        input_ready_event.clear()

async def decoupled_communication():
    program = ('python3', 'echo_user_while.py')
    process: Process = await asyncio.create_subprocess_exec(
        *program,
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE
    )

    input_ready_event = asyncio.Event()
    text_input = ['one\n', 'two\n', 'three\n', 'four\n', 'quit\n']

    await asyncio.gather(
        output_consumer(input_ready_event, process.stdout),
        input_writer(text_input, input_ready_event, process.stdin),
        process.wait()
    )

# ---

async def main():
    # await one_shot_stdin()
    # await continuous_communication()
    await decoupled_communication()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
