#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Required, Field

app = FastAPI()


# Fields are used to declare additional validation and metadata
# inside of Pydantic models using Pydantic's `Field`

class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put("/items{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

