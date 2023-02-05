#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header, HTTPException, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()

## 
# Exception handlers
#
# It is possible to register custom exception handlers.
# This might be useful to intercept any exceptions from third-party libraries.

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# Here, if `/unicorns/yolo` is requested, the path operation will raise a `UnicornException`.
# However, it will be handled by the `unicorn_exception_handled`,
# so we will receive a clean error, with an HTTP status code of 418.


# While developing an application it might be useful to handle any RequestValidationError's.
# That way we could log the body that cause the error, inspect it, etc.

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body})
    )



class Item(BaseModel):
    title: str
    size: int

@app.post("/items/")
async def create_item(item: Item):
    return item


# We can also just reuse fastapi's exception handlers:


class SomeOtherException(Exception):
    pass

@app.exception_handler(SomeOtherException)
async def some_other_exception_handler(request: Request, exc: SomeOtherException):
    print(f"OMG! we got an exception!: {exc}")
    return await request_validation_exception_handler(request, exc)
