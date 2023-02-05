#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set

from fastapi import FastAPI, Query, Path, Body, Cookie
from pydantic import BaseModel, Required, Field, HttpUrl

app = FastAPI()


# Cookie parameters are defined the same way Query and Path parameters are.


@app.get("/items/")
async def read_items(ads_id: Optional[str] = Cookie(default=None)):
    return {"ads_id": ads_id}
