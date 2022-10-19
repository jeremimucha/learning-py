#!/usr/bin/env python3

import asyncio
from aiohttp import ClientSession

from .timing import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str, delay: int = 0) -> int:
    if delay:
        await asyncio.sleep(delay)
    async with session.get(url) as result:
        return result.status
