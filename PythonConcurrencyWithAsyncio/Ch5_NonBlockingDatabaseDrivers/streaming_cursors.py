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


async def query_all_products(connection: asyncpg.Connection):
    query = 'SELECT product_id, product_name FROM product'
    async with connection.transaction():
        # Using a cursor we will only pull a few items from the database at a time.
        # This might be necessary for very large datasets.
        # The default prefetch is 50 records at a time.
        # This can be changed with the `prefetch` parameter.
        async for product in connection.cursor(query):
            print(product)


async def manipulate_cursor(connection: asyncpg.Connection):
    query = 'SELECT product_id, product_name FROM product'
    async with connection.transaction():
        # We don't need to iterate over the cursor immediately, simply create it.
        # The cursor is both an asynchronous generator and an awaitable.
        cursor = await connection.cursor(query)
        # Move cursor forward 500 records
        await cursor.forward(500)
        # Get the next 100 records
        products = await cursor.fetch(100)
        for product in products:
            print(product)



# If we want to get just a specific number of elements with an async generator:
async def take(generator, to_take: int):
    item_count = 0
    async for item in generator:
        if item_count > to_take - 1:
            return
        item_count += 1
        yield item

async def query_some(connection: asyncpg.Connection):
    async with connection.transaction():
        query = 'SELECT product_id, product_name FROM product'
        product_generator = connection.cursor(query)
        async for product in take(product_generator, 5):
            print(product)
        
        print('Got the first five products!')



async def main():
    connection: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1', port=5432, user='postgres', database='products', password='1234')

    # await query_all_products(connection)
    # await manipulate_cursor(connection)
    await query_some(connection)

    await connection.close()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
