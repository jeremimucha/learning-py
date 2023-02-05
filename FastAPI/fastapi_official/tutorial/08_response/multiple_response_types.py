#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any, Union, Dict

from fastapi import FastAPI, Query, Path, Body, Header
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


# Responses can be declared to be the `Union` of two types, that means,
# the response would be any of the two.
# This translates to `anyOf` on OpenAPI


class BaseItem(BaseModel):
    description: str
    type: str

class CarItem(BaseItem):
    type = "car"

class PlaneItem(BaseItem):
    type = "plane"
    size: int


items = {
    "item1": {"description": "All my friends drive a low rider", "type": "car"},
    "item2": {
        "description": "Music is my aeroplane, it's my aeroplane",
        "type": "plane",
        "size": 5,
    },
}

@app.get("/items/{item_id}", response_model=Union[PlaneItem, CarItem])
async def read_item(item_id: str):
    return items[item_id]


# It is also possible to declare responses of lists of objects.

class Item(BaseModel):
    name: str
    description: str

items2 = [
    {"name": "Foo", "description": "There comes my hero"},
    {"name": "Red", "description": "It's my aeroplane"},
]

@app.get("/items2/", response_model=List[Item])
async def read_items2():
    return items2


# A response_model may also be an arbitrary Dict.
# This can be useful for prototyping, when you might not want to declare a Pydantic model yet.
@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
