#!/usr/bin/env python3

from email import iterators
from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import asyncpg
import functools
import itertools
import random


create_user_cart_query = """
CREATE TABLE user_cart(
    user_id INT NOT NULL,
    product_id INT NOT NULL
);
"""

create_user_favorite_query = """
CREATE TABLE user_favorite(
    user_id INT NOT NULL,
    product_id INT NOT NULL
);
"""


async def insert_many_into(table_name: str, number_items: int, connection: asyncpg.Connection):
    item_tuples = []
    for _ in range(number_items):
        user_id = random.randint(1, 3)
        product_id = random.randint(1, 100)
        item_tuples.append((user_id, product_id))
    await connection.executemany(f'INSERT INTO {table_name} VALUES($1, $2)', item_tuples)


async def main():
    cart_conn: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1', port=5432, user='postgres', database='cart', password='1234')
    
    # try:
    #     # await cart_conn.execute(create_user_cart_query)
    #     await insert_many_into("user_cart", 10, cart_conn)
    # finally:
    #     await cart_conn.close()

    fav_conn: asyncpg.Connection = await asyncpg.connect(
        host='127.0.0.1', port=5432, user='postgres', database='favorites', password='1234')
    
    try:
        # await fav_conn.execute(create_user_favorite_query)
        await insert_many_into("user_favorite", 10, fav_conn)
    finally:
        await fav_conn.close()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
