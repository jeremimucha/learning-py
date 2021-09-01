#!/usr/bin/env python

# model.py  --  DB model for the sanic demo "patron" table.

import logging
from json import loads, dumps

from triggers import (create_notify_trigger, add_table_triggers)
from boltons.cacheutils import LRU


logger = logging.getLogger('perf')

CREATE_TABLE = ('CREATE TABLE IF NOT EXISTS patron('
                'id serial PRIMARY KEY, name text, '
                'fav_dish text')
INSERT = ('INSERT INTO patron(name, fav_dish) '
          'VALUES ($1, $2) RETURNING id')
SELECT = 'SELECT * FROM patron WHERE id = $1'
UPDATE = 'UPDATE patron SET name=$1, fav_dish=$2 WHERE id=$3'
DELETE = 'DELETE FROM patron WHERE id=$1'
EXISTS = "SELECT to_regclass('patron')"

CACHE = LRU(max_size=65536)
