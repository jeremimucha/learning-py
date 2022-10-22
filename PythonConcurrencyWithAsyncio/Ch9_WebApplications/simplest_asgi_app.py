#!/usr/bin/env python3

# Run with
# uvicorn simplest_asgi_app:application

async def application(scope, receive, send):
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'content-type', b'text/html']]
    })
    await send({'type': 'http.response.body', 'body': b'ASGI hello!'})
