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
import asyncpg
from concurrent.futures.process import ProcessPoolExecutor
from typing import Dict, List

from util import async_timed


# For work that is both IO and CPU bound it's possible to use ProcessPools
# that run their independent asyncio event loops so that each process gets
# a chunk of the work to do and handles the data it queries.
# This will not reduce the IO bound work that needs to be done,
# but will distribute it across processes, allowing the CPU bound work
# to also be distributed.


product_query = \
    """
SELECT
p.product_id,
p.product_name,
p.brand_id,
s.sku_id,
pc.product_color_name,
ps.product_size_name
FROM product as p
JOIN sku as s on s.product_id = p.product_id
JOIN product_color as pc on pc.product_color_id = s.product_color_id
JOIN product_size as ps on ps.product_size_id = s.product_size_id
WHERE p.product_id = 100"""


async def query_product(pool: asyncpg.Pool):
    async with pool.acquire() as connection:
        return await connection.fetchrow(product_query)


@async_timed()
async def query_products_concurrently(pool: asyncpg.Pool, queries):
    queries = [query_product(pool) for _ in range(queries)]
    return await asyncio.gather(*queries)


# Run queries in a new event loop and connection pool, and covert them to dictionaries.
# Conversion to dictionaries is necessary, since asyncpg Record objects can not be pickled.
def run_in_new_loop(num_queries: int) -> List[Dict]:
    async def run_queries():
        # New connection pool
        async with asyncpg.create_pool(host='127.0.0.1',
                                    port=5432,
                                    user='postgres',
                                    password='1234',
                                    database='products',
                                    min_size=6,
                                    max_size=6) as pool:
            return await query_products_concurrently(pool, num_queries)
    # New event loop
    results = [dict(result) for result in asyncio.run(run_queries())]
    return results


# This process launches the other processes and gets the results from them.
async def main():
    loop = asyncio.get_running_loop()
    pool = ProcessPoolExecutor()
    tasks = [loop.run_in_executor(pool, run_in_new_loop, 10000) for _ in range(5)]
    all_results = await asyncio.gather(*tasks)
    total_queries = sum([len(result) for result in all_results])
    print(f'Retrieved {total_queries} products from the product database')


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
