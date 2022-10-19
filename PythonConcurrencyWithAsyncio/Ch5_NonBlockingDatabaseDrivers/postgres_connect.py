#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import asyncpg


async def main():
    connection = await asyncpg.connect(
                        host='127.0.0.1',
                        port=5432,
                        user='postgres',
                        database='postgres',
                        password='1234'
                        )
    version = connection.get_server_version()
    print(f'Connected! Postgres version is{version}')
    await connection.close()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectoEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
