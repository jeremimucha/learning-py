#!/usr/bin/env python3

# This is a helper script meant to produce a whole lot of stdout output.
# Extensive amount of console output can cause deadlocks when piping with asyncio.subprocess
# see deadlock_with_pipes.py

if __name__ == '__main__':
    import sys
    [sys.stdout.buffer.write(b'Hello there!\n') for _ in range(1000000)]
    sys.stdout.flush()
