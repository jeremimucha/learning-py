#!/usr/bin/env python3
from enum import Enum
from fastapi import FastAPI
from typing import Optional


app = FastAPI()


# Parameters that are not part of the path parameters, are automatically interpreted as "query" parameters.
# Query is the set of key-value pairs that go after the `?` in a URL, separated by & characters.

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

# http://127.0.0.1:8000/items/?skip=20
# skip=20
# limit=10


# Parameters can be optional, by defaulting them to None.
# Boolean query parameters.
# - If a parameter is declared to be of type boolean, the usual "truthy" query values
#   will be converted to bool

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# All of the following would result in `short is True`
# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=True
# http://127.0.0.1:8000/items/foo?short=true
# http://127.0.0.1:8000/items/foo?short=on
# http://127.0.0.1:8000/items/foo?short=yes


# Multiple query an multiple path parameters may be used at the same time:

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
