#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response
import random


# Inventory service
# This contains a mapping from a product ID to the available inventory for that product.
# This implementation only emulates the service - returning a random available inventory count.


routes = web.RouteTableDef()

@routes.get('/products/{id}/inventory')
async def get_inventory(request: Request) -> Response:
    delay: int = random.randint(0, 5)
    await asyncio.sleep(delay)
    inventory: int = random.randint(0, 100)
    return web.json_response({'inventory': inventory})


def main():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8001)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    main()
