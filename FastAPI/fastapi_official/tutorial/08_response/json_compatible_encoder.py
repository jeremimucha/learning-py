#!/usr/bin/env python3
from enum import Enum
from datetime import datetime
from typing import Optional, List, Set, Any


from fastapi import FastAPI, Query, Path, Body, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()

# Sometimes it is necessary to convert a data type (e.g. a Pydantic model),
# to something compatible with JSON - dict, list, etc.
# For example to store it in a database.
# This is best done with `jsonable_encoder`.
#
# jsonable_encoder doesn't just dump everything to string like json.dumps() would.
# It returns a Python standard data structure, e.g. a `dict`, with values and sub-values
# that are all compatible with JSON.

fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: Optional[str] = None


# In this example the jsonable_encoder convers the Pydantic model to `dict` and the datetime to a `str`
@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
