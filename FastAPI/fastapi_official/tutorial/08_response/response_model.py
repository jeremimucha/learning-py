#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header
from pydantic import BaseModel, Required, Field, HttpUrl

app = FastAPI()


# Response Model type can be declared using return type annotation,
# the same way it is done for function parameters.
#
# To allow implicit conversions it is possible to use the `response_model`
# parameter, instead of the return type annotation for this purpose.
# Using the response_model allows e.g. Pydantic models to be converted
# to dictionaries and vice-versa.
# This works for all the path operations (decorators):
# * @app.get()
# * @app.post()
# * @app.put()
# * @app.delete()
# * etc.

# If both the return type and response_model are declared,
# the response_model takes priority.

# FastAPI will use this return type to:
# * Validate the returned data.
#   If the data is invalid (e.g. you are missing a field), it means that your app code is broken,
#   not returning what it should, and it will return a server error instead of returning incorrect data.
#   This way you and your clients can be certain that they will receive the data and the data shape expected.
# * Add a JSON Schema for the response, in the OpenAPI path operation.
#   This will be used by the automatic docs.
#   It will also be used by automatic client code generation tools.
# * It will limit and filter the output data to what is defined in the return type.
#   This is particularly important for security, we'll see more of that below.

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: List[str] = []


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> List[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


# Using response_model:

@app.post("/other_items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item

@app.get("/items/", response_model=List[Item])
async def read_items() -> Any:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]
