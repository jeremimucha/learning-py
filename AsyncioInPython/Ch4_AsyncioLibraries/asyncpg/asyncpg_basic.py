#!/usr/bin/env python

# Demo of asyncpg used to communicate with a PostgreSQL database.

import asyncio
import asyncpg
import datetime
from asyncpg_util import Database


async def main():
    async with Database('test', owner=True) as conn:
        await demo(conn)


async def demo(conn: asyncpg.Connection):
    await conn.execute('''
        CREATE TABLE users(
            id serial PRIMARY KEY,
            name text
            dob date
        )'''
    )

    # fetchval executes a query and returns the first row (id).
    pk = await conn.fetchval(
        # Note that params $1 $2 are used here - never use string
        # interpolation in DB queries as this is a security risk.
        # Same goes for concatenation.
        'INSERT INTO users(name, dob) VALUES($1, $2) '
        'RETURNING id', 'Bob', datetime.date(1984, 3, 1)
    )

    async def get_row():
        return await conn.fetchrow(
            'SELECT * FROM users WHERE name = $1',
            'Bob'
        )
    print('After INSERT:', await get_row())

    await conn.execute(
        'UPDATE users SET dob = $1 WHERE id=1',
        datetime.date(1985, 3, 1)
    )
    print('After UPDATE:', await get_row())

    await conn.execute(
        'DELETE FROM users WHERE id=1'
    )
    print('After DELETE:', await get_row())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down...")
