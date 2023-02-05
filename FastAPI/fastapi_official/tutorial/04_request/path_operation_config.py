#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header, Form, File, UploadFile, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()

# The Path() operation can be configured in various ways.
# - status_code - set the response status_code
# - tags - add tags to the operation -> List[str]
# - summary
# - description
# - response_description


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()

@app.post(
    "/items/",
    response_model=Item, status_code=status.HTTP_201_CREATED,
    tags=["items"],
    summary="Create an item",
    # The description is better left to be defined as a docstring of the function
    # description="Create an item with all the information, name, description, price, ...",
    response_description="The created item",
)
async def create_item(item: Item):
    # Docstrings are parsed and used as the operation description.
    # Markdown can be used.
    """
    Create an item with all the information:
    
    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
    return item

@app.get("/items/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
