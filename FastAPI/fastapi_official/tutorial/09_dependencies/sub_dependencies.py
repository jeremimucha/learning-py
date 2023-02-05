#!/usr/bin/env python3
from enum import Enum
from datetime import datetime
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Depends, Query, Path, Body, Header, HTTPException, status, Request, Cookie
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


# Dependencies can have arbitrarily nested sub-dependencies.

def query_extractor(q: Optional[str] = None):
    return q

def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = Cookie(default=None)
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}
