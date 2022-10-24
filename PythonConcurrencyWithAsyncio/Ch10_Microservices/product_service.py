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
import functools
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
from Ch10_Microservices.manage_conn_pool import (
    DB_KEY,
    create_database_pool,
    destroy_database_pool,
)


# Product service
# This contains product information, such as descriptions and SKUs.


routes = web.RouteTableDef()


@routes.get('/products')
async def products(request: Request) -> Response:
    db = request.app[DB_KEY]
    product_query = 'SELECT product_id, product_name FROM product'
    result = await db.fetch(product_query)
    return web.json_response([dict(record) for record in result])


def main():
    app = web.Application()
    app.on_startup.append(functools.partial(create_database_pool,
                                            host='127.0.0.1',
                                            port=5432,
                                            user='postgres',
                                            password='1234',
                                            database='products'))
    app.on_cleanup.append(destroy_database_pool)

    app.add_routes(routes)
    web.run_app(app, port=8000)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
