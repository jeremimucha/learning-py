#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


# To return a reponse with errors to the client use HTTPException

items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        # The `detail` can be any object that is serializable to JSON.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item": items[item_id]}


# In some situations it might be necessary to include custom headers.
# This is as simple as:

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",
            headers={"X-Error": "There goes my error"}
        )
    return {"item": items[item_id]}

