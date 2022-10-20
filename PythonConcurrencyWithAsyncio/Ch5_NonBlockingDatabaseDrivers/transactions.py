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
from asyncpg.transaction import Transaction


# Transactions are meant to ensure atomic operations on the database.
# If everything goes fine the transaction is commited, if something fails it's rolled-back.
# With asyncpg this is done using async context manager - `connection.transaction()`.


async def insert_success(connection: asyncpg.Connection):
    # Start a transaction
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")

    query = "SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'"
    brands = await connection.fetch(query)
    print(brands)


async def insert_error(connection: asyncpg.Connection):
    try:
        async with connection.transaction():
            insert_brand = "INSERT INTO brand VALUES(9999, 'big_brand')"
            await connection.execute(insert_brand)
            # The second insert will fail due to an already existing id
            # Since we're operating in the context of a transaction, a failure of this second query
            # will result in a rollback of the first query.
            await connection.execute(insert_brand)
    except Exception:
        print('Error while running transaction')
    finally:
        query = "SELECT brand_name FROM brand WHERE brand_name LIKE 'big_%'"
        brands = await connection.fetch(query)
        print(f'Query result was: {brands}')


# asyncpg also supports the concept of a `nested transaction` through Postgres feature called `savepoints`.
# SAVEPOINTS define a point within the transaction process that can be rolled-back to.
# If a savepoint is created and a subsequent transaction fails, all the transactions executed after the savepoint
# was created will be rolled back to the savepoint, but all the transactions executed before the savepoint
# will not be rolled back.
# With asyncpg this is done simply by nesting `connection.transaction()` context managers.

async def insert_with_savepoint(connection: asyncpg.Connection):
    async with connection.transaction():
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'my_new_brand')")

        try:
            # This nested transaction will fail and we'll roll back to this point.
            async with connection.transaction():
                await connection.execute("INSERT INTO product_color VALUES(1, 'black')")
        except Exception as ex:
            print(f'Ignoring error inserting product color {ex}')

    # The outer transaction was still commited:
    query = "SELECT brand_name FROM brand WHERE brand_name LIKE 'my_new_%'"
    brands = await connection.fetch(query)
    print(f'Queryt result was: {brands}')


# Manualy managing transactions - sometimes necessary if custom code on transaction success/failure is needed.
async def explicit_transaction_management(connection: asyncpg.Connection):
    # Create a transaction instance
    transaction: Transaction = connection.transaction()
    # Since we're no longer using the transaction as a context manager we need to start it.
    await transaction.start()
    try:
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'brand_2')")
    except asyncpg.PostgresError:
        print('Errors, rolling back transaction!')
        await transaction.rollback()
    else:
        print('No errors, commiting transaction!')
        await transaction.commit()

    query = "SELECT brand_name FROM brand WHERE brand_name LIKE 'brand%'"
    brands = await connection.fetch(query)
    print(brands)


async def main():
    connection: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1', port=5432, user='postgres', database='products', password='1234')

    # await insert_success(connection)
    # await insert_error(connection)
    # await insert_with_savepoint(connection)
    await explicit_transaction_management(connection)

    await connection.close()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
