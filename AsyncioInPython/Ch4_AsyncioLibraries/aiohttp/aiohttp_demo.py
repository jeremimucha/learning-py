#! /usr/bin/env python

# A simple application demonstrating how to set up an http server using aiohttp
# Note that everything is encapsulated - there's no mention of loops or executors.

from aiohttp import web


async def hello(request):
    return web.Response(text="Hello world")


if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', hello)
    web.run_app(app, port=8080)
