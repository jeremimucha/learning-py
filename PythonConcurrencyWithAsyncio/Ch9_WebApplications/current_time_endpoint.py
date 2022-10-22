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
from datetime import datetime


# Define the routes (endpoints) for the application
routes = web.RouteTableDef()


# Create a time GET endpoint.
# When a client calls this endpoint, the time coroutine will run.
@routes.get('/time')
async def time(request: Request) -> Response:
    print(request.headers)
    
    today = datetime.today()

    result = {
        'month': today.month,
        'day': today.day,
        'time': str(today.time())
    }

    # Take the result dictionary and turn it into a JSON response.
    # The status_code is set to `200`
    # Content type is set to `application/json`
    return web.json_response(result)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Create the web application, register the routes and run the application
    app = web.Application()
    app.add_routes(routes)
    # By default the web server is started on localhost:8080
    web.run_app(app)
