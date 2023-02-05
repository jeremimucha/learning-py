#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set

from fastapi import FastAPI, Query, Path, Body, Header
from pydantic import BaseModel, Required, Field, HttpUrl

app = FastAPI()


# Header parameters are declared using the `Header` type.
# Because standard headers use "hyphen" as the separator - e.g. `user-agent`,
# but user-agent is an invalid python identifier, the `Header` type by default
# converts parameter names from underscores to hyphens:
# * user_agent -> user-agent
# The automatic conversion can be suppressed:
# * convert_underscores=False

@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(default=None)):
    return {"User-Agent": user_agent}


# Sometimes headers can appear multiple times, with different values.
# This is supported by declaring the Header of type List[str]

@app.get("/items/")
async def read_items(x_token: Optional[List[str]] = Header(default=None)):
    return {"X-Token values": x_token}
