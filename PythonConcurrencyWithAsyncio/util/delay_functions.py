import asyncio


async def delay(delay_seconds: int) -> int:
    print(f"Sleeping for {delay_seconds} second(s)")
    await asyncio.sleep(delay_seconds)
    print(f"Finished sleeping for {delay_seconds} second(s)")
    return delay_seconds
