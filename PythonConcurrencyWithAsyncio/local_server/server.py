#!/usr/bin/env python3

from fastapi import FastAPI


app = FastAPI()


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/")
async def index():
    return
