#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Required, Field

app = FastAPI()


# Example data for pydantic models can be declared using `Config` and `schema_extra`
# Extra info can also be declared for the JSON Schema, by passing any other arbitrary arguments to the function.
# This can be used to add `example` for each field
# This doesn't add any extra validation and just serves as documentation.


class Item(BaseModel):
    name: str = Field(example="Foo")
    description: Optional[str] = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: Optional[float] = Field(default=None, example=3.2)

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        example={
            "name": "Foo",
            "description": "A very nice Item",
            "price": 35.3,
            "tax": 3.2,
        }
    )
):
    results = {"item_id": item_id, "item": Item}
    return results


# An alternative to specifying a single example is to specify `examples` using a dict.
# This provides extra information that will be added to OpenAPI.
# Each dict in the examples can contain:
# - `summary` - short description of the example
# - `description` - A long description that can contain Markdown text
# - `value` - This is the eactual example show
# - `externalValue`: alternative to `value`, a URL pointing to the example.

@app.put("/different/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": Item}
    return results