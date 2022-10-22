#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
from starlette.applications import Starlette
from starlette.websockets import WebSocket
from starlette.endpoints import WebSocketEndpoint
from starlette.routing import WebSocketRoute
from typing import Any


# Example of a WebSocket application.
# The app maintains a list of all connected client WebSockets.
# When a new client connects, they're added to the list and all connected clients receive
# an updated count of users.
# When a client disconnects, they're removed from the list and all other clients receive
# an updated cout of users.


class UserCounter(WebSocketEndpoint):
    encoding = 'text'
    sockets = []

    # When a client connects, add it to the list of sockets, and notify other users of the new count.
    async def on_connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        UserCounter.sockets.append(websocket)
        await self._send_count()

    # When a client disconnects, remove it from the list of sockets and notify other users of the new count.
    async def on_disconnect(self, websocket: WebSocket, close_code: int) -> None:
        UserCounter.sockets.remove(websocket)
        await self._send_count()

    async def on_receive(self, websocket: WebSocket, data: Any) -> None:
        pass

    # Notify users how many users are connected.
    # If there is an exception while sending, remove them from the list.
    async def _send_count(self):
        if len(UserCounter.sockets) > 0:
            count_str = str(len(UserCounter.sockets))
            task_to_socket = {
                asyncio.create_task(websocket.send_text(count_str)): websocket
                for websocket in UserCounter.sockets
            }

        done, pending = await asyncio.wait(task_to_socket)

        for task in done:
            if task.exception() is not None:
                if task_to_socket[task] in UserCounter.sockets:
                    UserCounter.sockets.remove(task_to_socket[task])


app = Starlette(
    routes=[WebSocketRoute('/counter', UserCounter)]
)
