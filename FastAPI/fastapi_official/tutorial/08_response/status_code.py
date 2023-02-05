#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header, status
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


# It is possible to explicitly specify the response HTTP status code.
# By default 200 is returned on successfull response, which might not
# be exactly correct.

@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}
