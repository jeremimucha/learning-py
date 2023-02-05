#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List

from fastapi import FastAPI, Query
from pydantic import BaseModel, Required


app = FastAPI()


# The `Query` type provides a way to perform additional validation on parameters


@app.get("/items/")
async def read_items(q: Optional[str] = Query(default=None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id", "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# The following query allows only `q` arguments matching the given regex.
@app.get("/items-with-regex/")
async def read_items(q: Optional[str] = Query(default=None, min_length=3, max_length=50, regex="^fixedquery$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id", "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# A Query argument without a `default=` value is required.
# The same can be achieved by explicitly setting `default=...` (ellipsis),
# Or by using Pydantic's `Required` - `default=Required`
@app.get("/items-required/")
async def read_items(q: str = Query(default=..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id", "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# A Query parameter can be declared to allow multiple occurrences in a path.
# This is done by typing the parameter as a List[...]
#
# Given `http://localhost:8000/items/?q=foo&q=bar`
# We'd get `q == ["foo", "bar"]`

@app.get("/items-multiple")
async def read_items(q: Optional[List[str]] = Query(default=None)):
    query_items = {"q", q}
    return query_items


# Queries can include significantly more metadata, like
# - title
# - description
# - alias - creating path parameters that are otherwise not valid python identifiers

@app.get("/items-query-alias")
async def read_items(q: Optional[str] = Query(
        default=None,
        alias="item-query",
        title="Query string",
        description="Query string for the items to search in the database that have a good match.",
        min_length=3,
        # deprecated=True           # mark the paramater as deprecated in the documentation
        # include_in_schema=False   # remove it entirely from the documentation
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
