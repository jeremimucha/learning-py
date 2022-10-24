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

# Favorite service
# This service keeps track of a mapping from a user to the product IDs they have put in their favorites list.


routes = web.RouteTableDef()


@routes.get('/users/{id}/favorites')
async def favorites(request: Request) -> Response:
    try:
        str_id = request.match_info['id']
        user_id = int(str_id)
        db = request.app[DB_KEY]
        favorite_query = 'SELECT product_id from user_favorite where user_id = $1'
        result = await db.fetch(favorite_query, user_id)
        if result is not None:
            return web.json_response([dict(record) for record in result])
        else:
            raise web.HTTPNotFound()
    except ValueError:
        raise web.HTTPBadRequest()


app = web.Application()
app.on_startup.append(functools.partial(create_database_pool,
                                        host='127.0.0.1',
                                        port=5432,
                                        user='postgres',
                                        password='1234',
                                        database='favorites'))
app.on_cleanup.append(destroy_database_pool)

app.add_routes(routes)
web.run_app(app, port=8002)
