#!/usr/bin/env python3
from enum import Enum
from typing import Optional, List, Set, Any

from fastapi import FastAPI, Query, Path, Body, Header, Form, File, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Required, Field, HttpUrl, EmailStr

app = FastAPI()

# It is possible to define files to be uploaded by the client
# using File and UploadFile.
# * File inherits directly from Form.
# * The files will be uploaded as "form data"
# * The parameter should be declared as type `bytes`
#   This will cause fastapi to read the file and pass the content as bytes.
# * File causes the entire contents to be read and stored in memory.
# * For larger files use UploadFile - this is a "spooled" file handle,
#   stores a chunk of the file in memory and streams from disk as necessary.
#   - Has an async file-like interface.
#   - Exposes Python's `SpooledTemporaryFile` object


@app.post("/files/")
async def create_file(file: bytes = File()):
    return {"file_size": len(file)}


@app.post("/uploadFile/")
async def create_upload_file(file: UploadFile = File(description="This is just metadata")):
    return {"filename": file.filename}


# Multiple file uploads are just a `List[bytes] = File()` or `List[UploadFile]`
@app.post("/more-files/")
async def create_files(files: List[bytes] = File(description="Multiple files as bytes")):
    return {"file_sizes": [len(file) for file in files]}

@app.post("/more-uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(description="Multiple files as UploadFile")):
    return {"filenames": [file.filename for file in files]}

@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
