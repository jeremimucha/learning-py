#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Required

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    item: Optional[Item] = None,
    user: User,
    importance: int = Body(),
    q: Optional[str] = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


# Multiple body parameters end up being used as keys in the body:
# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     },
#     "user": {
#         "username": "dave",
#         "full_name": "Dave Grohl"
#     },
#    "importance": 5
# }


# If we have only a single Body parameter, but we still want it to be
# represented as a JSON with a key=<body-parameters>,
# this can be achieved using the `Body(embed=True)` parameter.
@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
    item: Item = Body(embed=True),
):
    results = {"item_id": item_id, "item": item}
    return results

# This will result in:

# {
#     "item": {
#         "name": "Foo",
#         "description": "The pretender",
#         "price": 42.0,
#         "tax": 3.2
#     }
# }

# Instead of

# {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
# }

