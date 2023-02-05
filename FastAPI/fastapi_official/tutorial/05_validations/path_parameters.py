#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, Required


app = FastAPI()


# Path allows for additional validation and metadata for path parameters.


@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get"),
    q: Optional[str] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


# For numerical values, Path allows for a checke of the range of the value:
# - gt - greather than,
# - ge - greater equal,
# etc.
@app.get("/items/{item_id}")
async def read_items(
    *,  # A trick to order the parameters the way we want, regardless of if they have a default value
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: str,
    size: float = Query(gt=0, lt=10.5),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
