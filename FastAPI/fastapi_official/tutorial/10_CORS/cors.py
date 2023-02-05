#!/usr/bin/env python3
from enum import Enum
from datetime import datetime
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Depends, Query, Path, Body, Header, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()


# CORS - Cross Origin Resource Sharing
# - Frontend running in a browser has JavaScript code that communicates with a backedn, and the backend
#   is in a different "origin" than the frontend.

# Origin - combination of:
# - protocol - http, https,
# - domain - myapp.com, localhost,
# - port 80, 443, 8080,
#
# All of these are different origins, even though they're all localhost:
# - http://localhost
# - https://localhost
# - http://localhost:8080

# CORS in FastAPI is configured using CORSMiddleware
#
# - Create a list of allowed origins (as strings).
# - Add it as a "middleware" to your FastAPI application.
#
# You can also specify if your backend allows:
# - Credentials (Authorization headers, Cookies, etc).
# - Specific HTTP methods (POST, PUT) or all of them with the wildcard "*".
# - Specific HTTP headers or all of them with the wildcard "*".

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.get("/")
async def main():
    return {"message": "Hello World"}
