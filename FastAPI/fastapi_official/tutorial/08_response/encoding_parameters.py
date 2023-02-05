#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


# It is possible to omit elements from the result if they are not actually stored
# by setting the `response_model_exclude_unset` parameter.
# This might be benefitial e.g. in case of models with many optional attributes
# when using NoSQL database. This way we can avoid the need to send very long
# JSON responses full of default values.

# Internally this is achieved using Pydantic's .dict() using `exclude_unset`.


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: float = 10.5
    tags: List[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]

# In the above example only explicitly set fields will be included in the response.
