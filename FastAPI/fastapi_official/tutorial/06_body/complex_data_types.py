#!/usr/bin/env python3
from enum import Enum
from datetime import datetime, time, timedelta
from typing import Optional, List
from uuid import UUID

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Required, Field

app = FastAPI()


# In addition to simple built-in data types, fastapi supports
# more complex data types, while still providing data conversion,
# data validation, automatic annotation and documentation.

# UUID
# datetime.datetime
# datetime.date
# datetime.time
# datetime.timedelta
# frozenset
# bytes
# Decimal


# NOTE:
# - The `Body` parameter in the following example is used, because for singular parameters
#   fastapi otherwise assumes they're query or path parameters. `Body` forces the param to be part of the body.


@app.put("/items/{item_id}")
async def read_times(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(default=None),
    end_datetime: Optional[datetime] = Body(default=None),
    repeat_at: Optional[time] = Body(default=None),
    process_after: Optional[timedelta] = Body(default=None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }