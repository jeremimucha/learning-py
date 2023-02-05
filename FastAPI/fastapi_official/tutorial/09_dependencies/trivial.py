#!/usr/bin/env python3
from enum import Enum
from datetime import datetime
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Depends, Query, Path, Body, Header, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


async def common_parameters(
    q: Optional[str] = None, skip: int = 0, limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
