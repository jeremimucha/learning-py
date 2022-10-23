#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from enum import Enum


# Example demonstrating the use of a Condition to manage a database connection to run queries.
# We have an underlying connection that can't run multiple queries at the same time,
# and the database connection may not be initialized before someone tries to run a query.


class ConnectionState(Enum):
    WAIT_INIT = 0
    INITIALIZING = 1
    INITIALIZED = 2


class Connection:

    def __init__(self):
        self._state = ConnectionState.WAIT_INIT
        self._condition = asyncio.Condition()

    async def initialize(self):
        await self._change_state(ConnectionState.INITIALIZING)
        print('initialize: Initializing connection...')
        await asyncio.sleep(3) # simulate connection startup time
        print('initialize: Finished initializing connection')
        await self._change_state(ConnectionState.INITIALIZED)

    async def execute(self, query: str):
        async with self._condition:
            print('execute: Waiting for connection to initialize')
            # Wait until a specific predicate is met.
            await self._condition.wait_for(self._is_initialized)
            print(f'execute: Running {query}!')
            await asyncio.sleep(3)

    async def _change_state(self, state: ConnectionState):
        async with self._condition:
            print(f'change_state: State changing from {self._state} to {state}')
            self._state = state
            self._condition.notify_all()

    def _is_initialized(self):
        if self._state is not ConnectionState.INITIALIZED:
            print(f'_is_initialized: Connection not finished initializing, state is {self._state}')
            return False
        print(f'_is_initialized: Connection is initialized!')
        return True


async def run_connection():
    connection = Connection()
    query_one = asyncio.create_task(connection.execute('SELECT * FROM foo'))
    query_two = asyncio.create_task(connection.execute('SELECT * FROM bar'))
    init = asyncio.create_task(connection.initialize())
    await asyncio.gather(init, query_one, query_two)


async def main():
    await run_connection()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
