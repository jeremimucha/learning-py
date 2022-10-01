"""
schedule_v4.py: homegrown cached property for speakers

    >>> event = Record.fetch('event.33950')

# tag::SCHEDULE4_DEMO[]
    >>> event  # <1>
    <Event 'There *Will* Be Bugs'>
    >>> event.venue  # <2>
    <Record serial=1449>
    >>> event.venue.name  # <3>
    'Portland 251'
    >>> for spkr in event.speakers:  # <4>
    ...     print(f'{spkr.serial}: {spkr.name}')
    3471: Anna Martelli Ravenscroft
    5199: Alex Martelli

# end::SCHEDULE4_DEMO[]
"""

import inspect
import json

JSON_PATH = 'data/osconfeed.json'

class Record:

    __index = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    @staticmethod
    def fetch(key):
        if Record.__index is None:
            Record.__index = load()
        return Record.__index[key]


class Event(Record):

    def __repr__(self):
        try:
            return f'<{self.__class__.__name__} {self.name!r}>'
        except AttributeError:
            return super().__repr__()

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        return self.__class__.fetch(key)

# tag::SCHEDULE4_HASATTR_CACHE[]
    @property
    def speakers(self):
        # Caching is commonly expected of properties, because expressions like
        # `event.venue` should generally be inexpensive.
        # The issue with handmade caches like this, is that they introduce
        # race conditions in threaded code.
        # Python3.8 introduced `functools.cached_property` decorator,
        # see schedule_v5.py
        #
        # If the instance doesn't have an attribute named __speakers_objs,
        # fetch the speaker objects and store them there.
        if not hasattr(self, '__speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self.__speaker_objs = [fetch(f'speaker.{key}')
                    for key in spkr_serials]
        # Then just return the speaker_objs
        return self.__speaker_objs

# end::SCHEDULE4_HASATTR_CACHE[]


def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, Record)
        if inspect.isclass(cls) and issubclass(cls, Record):
            factory = cls
        else:
            factory = Record
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)
    return records
