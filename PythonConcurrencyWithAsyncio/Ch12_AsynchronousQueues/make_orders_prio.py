#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession(base_url='http://127.0.0.1:8000') as session:
        # Plain user requests
        orders = [session.post('/order', data='{"power_user":"False"}') for _ in range(11)]
        # Power user requests added later, but should be processed first
        orders.extend([session.post('/order', data='{"power_user":"True"}') for _ in range(9)])

        await asyncio.gather(*orders)
        
        # orders_iter = asyncio.as_completed(orders)
        # for done_order in orders_iter:
        #     result = await done_order
        #     print(f'Order result: {result}')

        # done, pending = await asyncio.wait([asyncio.create_task(order) for order in orders])

        # for done_task in done:
        #     result = await done_task
        #     print(result)

if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(main())
