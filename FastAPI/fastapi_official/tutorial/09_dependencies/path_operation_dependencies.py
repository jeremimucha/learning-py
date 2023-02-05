#!/usr/bin/env python3
from enum import Enum
from datetime import datetime
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Depends, Query, Path, Body, Header, HTTPException, status, Request, Cookie
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


async def verify_token(x_toekn: str = Header()):
    if x_toekn != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")

async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
