#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header, Form
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


# It is possible to receive form fields, instead of JSON.
# This is done using the `Form` parameter - representing HTML `<form></form>`
# A request with Form parameters will have the body encoded using
# `application/x-www-form-urlencoded` instead of `application/json`.


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}


# E.g. OAuth2 "password flow" specification requires to send `username` and `password` as form fields.
# The fields need to be named exactly "username" and "password" and need to be Fields, not JSON.

