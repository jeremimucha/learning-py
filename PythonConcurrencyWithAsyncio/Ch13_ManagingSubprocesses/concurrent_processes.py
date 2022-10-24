#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from asyncio import Semaphore
from asyncio.subprocess import Process
import random
import string
import time


async def encrypt(sem: Semaphore, text: str) -> bytes:
    program = ('gpg', '-c', '--batch', '--passphrase', '3ncryptm3', '--cipher-algo', 'TWOFISH')

    # Limit the number of processes we start concurrently, so that we don't choke the CPU.
    async with sem:
        process: Process = await asyncio.create_subprocess_exec(
            *program,
            stdout=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE
        )

        # The bytes that we pass into the .communicate() will get piped into stdin of the subprocess,
        # as if we used `echo some-text | <subporocess>`.
        stdout, stderr = await process.communicate(text.encode())
        return stdout

async def main():
    text_list = [''.join(random.choice(string.ascii_letters) for _ in range(1000))
                 for _ in range(100)]
    
    semaphore: Semaphore = Semaphore(os.cpu_count())
    start = time.time()
    tasks = [asyncio.create_task(encrypt(semaphore, text)) for text in text_list]
    encrypted_text = await asyncio.gather(*tasks)
    end = time.time()

    print(f'Total time: {end - start}')
    # print(encrypted_text)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
