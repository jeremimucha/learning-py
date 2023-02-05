#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Optional[str] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


# Here, because we declare the response_model=UserOut, and return UserIn
# fastapi will take care of filtering out all the data that is not declared
# in the output model (using Pydantic internally).
@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user


# A better alternative to the above might be to use inheritance,
# and factor-out the common User part into a base class.
# That lets us annotate the return type precisely, so that we can
# benefit from type inference.

class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(BaseUser):
    password: str


@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user
