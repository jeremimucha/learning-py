#!/usr/bin/env python3


import asyncio

async def add_one(number: int) -> int:
    return number + 1


async def main() -> None:
    a = await add_one(1)
    b = await add_one(2)
    print(a)
    print(b)


if __name__ == '__main__':
    asyncio.run(main())
