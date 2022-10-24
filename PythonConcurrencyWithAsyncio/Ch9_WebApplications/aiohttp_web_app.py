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
from aiohttp import web
from aiohttp.web_app import Application
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import asyncpg
from asyncpg import Record
from asyncpg.pool import Pool
from typing import (List, Dict)


routes = web.RouteTableDef()
DB_KEY = 'database'


# aiohttp.web_app.Application can hold references to various data that we might need in the application endpoints.
# This lets us avoid using global variables, while still making the data available across the application.
# Here, this feature is used to hold a database connection pool.
# The pool needs to be created within the lifetime of the application (while its running on an event loop).
# This can be done using the `.on_startup` and `.on_cleanup` properties of the Application class.
# Any coroutines appended to these properties will run on startup or cleanup respectively.


# Create the database pool, and store it in the application instance.
async def create_database_pool(app: Application):
    print('Creating database pool')
    pool: Pool = await asyncpg.create_pool(host='127.0.0.1',
                                           port=5432,
                                           user='postgres',
                                           password='1234',
                                           database='products',
                                           min_size=6,
                                           max_size=6)
    app[DB_KEY] = pool

# Destroy the pool in the application instance.
async def destroy_database_pool(app: Application):
    print('Destroying database pool.')
    pool: Pool = app[DB_KEY]
    await pool.close()


# Query all brands and return results to the client.
@routes.get('/brands')
async def brands(request: Request) -> Response:
    connection: Pool = request.app[DB_KEY]
    brand_query = 'SELECT brand_id, brand_name FROM brand'
    results: List[Record] = await connection.fetch(brand_query)
    result_as_dict: List[Dict] = [dict(brand) for brand in results]
    return web.json_response(result_as_dict)


@routes.get('/products/{id}')
async def get_product(request: Request) -> Response:
    try:
        # Get the product id from the request URL
        str_id = request.match_info['id']
        product_id = int(str_id)
        
        query = \
            """
            SELECT
            product_id,
            product_name,
            brand_id
            FROM product
            WHERE product_id = $1
            """
        
        connection: Pool = request.app[DB_KEY]
        # Run the query for a single product
        result: Record = await connection.fetchrow(query, product_id)

        # If we have a result, convert it to JSON and send to the client.
        # Otherwise, send a "404 not found" status code
        if result is not None:
            return web.json_response(dict(result))
        else:
            raise web.HTTPNotFound()
    except ValueError:
        # Raising an exception appropriate for the situation will result in
        # the matching HTTP status code being returned, here - 400.
        raise web.HTTPBadRequest()

@routes.post('/product')
async def create_product(request: Request) -> Response:
    PRODUCT_NAME = 'product_name'
    BRAND_ID = 'brand_id'

    if not request.can_read_body:
        raise web.HTTPBadRequest()
    
    body = await request.json()

    if PRODUCT_NAME in body and BRAND_ID in body:
        db = request.app[DB_KEY]
        await db.execute(
            "INSERT INTO PRODUCT(product_id, product_name, brand_id) VALUES(DEFAULT, $1, $2)",
            body[PRODUCT_NAME],
            int(body[BRAND_ID])
        )
        return web.Response(status=201)
    else:
        raise web.HTTPBadRequest()


def main():
    app = web.Application()
    app.on_startup.append(create_database_pool)
    app.on_cleanup.append(destroy_database_pool)

    app.add_routes(routes)
    web.run_app(app)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
