#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
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

# User cart service
# Mapping from user ID to product IDs they have put in the cart; the data model is the same
# as the user favorite service.


routes = web.RouteTableDef()


@routes.get('/users/{id}/cart')
async def cart(request: Request) -> Response:
    try:
        str_id = request.match_info['id']
        user_id = int(str_id)
        db = request.app[DB_KEY]
        cart_query = 'SELECT product_id from user_cart where user_id = $1'
        result = await db.fetch(cart_query, user_id)
        if result is not None:
            return web.json_response([dict(record) for record in result])
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()


def main():
    app = web.Application()
    app.on_startup.append(functools.partial(create_database_pool,
                                            host='127.0.0.1',
                                            port=5432,
                                            user='postgres',
                                            password='1234',
                                            database='cart'))
    app.on_cleanup.append(destroy_database_pool)

    app.add_routes(routes)
    web.run_app(app, port=8003)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
