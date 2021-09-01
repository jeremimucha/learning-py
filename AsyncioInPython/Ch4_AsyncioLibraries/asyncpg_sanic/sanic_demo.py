#!/usr/bin/env python

import argparse
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.response import json
from util import Database


app = Sanic()


async def new_patron(request):
    data = request.json
    id = await model.add_patron(app.pool, data)
    return json(dict(msg='ok', id=id))
