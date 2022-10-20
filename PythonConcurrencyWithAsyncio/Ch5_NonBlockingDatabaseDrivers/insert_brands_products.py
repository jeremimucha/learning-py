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
import random
from asyncpg import Record
from typing import Any, List, Tuple, Union

sys.path.append(str(_SCRIPT))
from statements import *


async def insert_example(connection: asyncpg.Connection):
    # Insert data into the table
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Levis')")
    await connection.execute("INSERT INTO brand VALUES(DEFAULT, 'Seven')")

    # use a fetch query to get the inserted data
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[Record] = await connection.fetch(brand_query)
    # Or use .fetchrow() to get a single record from the query.

    for brand in results:
        print(f'id: {brand["brand_id"]}, name: {brand["brand_name"]}')


# We'd like to insert a large amount of generated brand names, to avoid listing them by hand.
def load_common_words() -> List[str]:
    with open(_SCRIPT/'common_words.txt') as common_words:
        return common_words.readlines()

def generate_brand_names(words: List[str]) -> List[Tuple[Union[str, Any]]]:
    return [(words[index],) for index in random.sample(range(100), 100)]


# .executemany() lets us execute a single query with multiple datasets
async def insert_brands(common_words, connection) -> int:
    brands = generate_brand_names(common_words)
    insert_brands = "INSERT INTO brand VALUES(DEFAULT, $1)"
    return await connection.executemany(insert_brands, brands)


def gen_products(common_words: List[str],
                 brand_id_start: int,
                 brand_id_end: int,
                 products_to_create: int) -> List[Tuple[str, int]]:
    products = []
    for _ in range(products_to_create):
        description = [common_words[index] for index in random.sample(range(1000), 10)]
        brand_id = random.randint(brand_id_start, brand_id_end)
        products.append((" ".join(description), brand_id))
    return products

def gen_skus(product_id_start: int,
             product_id_end: int,
             skus_to_create: int) -> List[Tuple[int, int, int]]:
    skus = []
    for _ in range(skus_to_create):
        product_id = random.randint(product_id_start, product_id_end)
        size_id = random.randint(1, 3)
        color_id = random.randint(1, 2)
        skus.append((product_id, size_id, color_id))
    return skus


async def insert_products(common_words: List[str], connection: asyncpg.Connection):
    product_tuples = gen_products(common_words, brand_id_start=1, brand_id_end=100, products_to_create=1000)
    await connection.executemany("INSERT INTO product VALUES(DEFAULT, $1, $2)", product_tuples)


async def insert_skus(connection: asyncpg.Connection):
    sku_tuples = gen_skus(product_id_start=1, product_id_end=100, skus_to_create=1000)
    await connection.executemany("INSERT INTO sku VALUES(DEFAULT, $1, $2, $3)", sku_tuples)


async def main():
    connection = await asyncpg.connect(
        host='127.0.0.1', port=5432, user='postgres', database='products', password='1234')
    
    await insert_example(connection)
    
    common_words = load_common_words()
    await insert_brands(common_words, connection)

    await insert_products(common_words, connection)
    await insert_skus(connection)

    await connection.close()


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
