"""
schedule_v2.py: property to get venue linked to an event

# tag::SCHEDULE2_DEMO[]
    >>> event = Record.fetch('event.33950')  # <1>
    >>> event  # <2>
    <Event 'There *Will* Be Bugs'>
    >>> event.venue  # <3>
    <Record serial=1449>
    >>> event.venue.name  # <4>
    'Portland 251'
    >>> event.venue_serial  # <5>
    1449

# end::SCHEDULE2_DEMO[]
"""

# tag::SCHEDULE2_RECORD[]
import inspect  # Used in `load()`
import json

JSON_PATH = 'data/osconfeed.json'

class Record:

    __index = None  # private class attribute will eventually hold a reference to the dict returned by load

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

    # Staticmethod to make it explicit that its effect is not influenced
    # by the instance or class on which it is called.
    @staticmethod
    def fetch(key):
        # Populate the Record.__index if needed
        if Record.__index is None:
            Record.__index = load()
        # Use it to retrieve the record with the given key.
        return Record.__index[key]
# end::SCHEDULE2_RECORD[]


# tag::SCHEDULE2_EVENT[]
# Event extends Record
class Event(Record):

    def __repr__(self):
        try:
            # If the instance has a name attribute, it is used to produce a custom representation.
            # Otherwise, delegate to the __repr__ from Record.
            return f'<{self.__class__.__name__} {self.name!r}>'
        except AttributeError:
            return super().__repr__()

    @property
    def venue(self):
        key = f'venue.{self.venue_serial}'
        # The venue property builds a key from the `venue_serial` attribute,
        # and passes it to the fetch class method, inherited from Record.
        # We go through the __class__ member here, accounting for a possibility
        # that the dataset contains a key named `fetch`. Going through __class__
        # guarantees that we will get the method, and not the dataset key.
        return self.__class__.fetch(key)
# end::SCHEDULE2_EVENT[]

# tag::SCHEDULE2_LOAD[]
def load(path=JSON_PATH):
    records = {}
    with open(path) as fp:
        raw_data = json.load(fp)
    for collection, raw_records in raw_data['Schedule'].items():
        record_type = collection[:-1]
        # Capitalize the `record_type` to get a possible class name,
        # e.g. `event` becomes `Event`.
        cls_name = record_type.capitalize()
        # Get an object by that name from the module global scope;
        # get the Record class if there's no such object.
        cls = globals().get(cls_name, Record)
        # If the retrieved object is a class and a subclass of Record
        if inspect.isclass(cls) and issubclass(cls, Record):
            # bind the factory name to it. This means `factory` may be any subclass
            # of Record, depending on `record_type`.
            factory = cls
        else:
            # Otherwise bind the factory to Record
            factory = Record
        # The for loop creates keys ands saves the records,
        # however, objects stored in records are constructed by `factory`,
        # which may be Record, or a subclass like Event, selected according to the record_type.
        for raw_record in raw_records:
            key = f'{record_type}.{raw_record["serial"]}'
            records[key] = factory(**raw_record)  # <8>
    return records
# end::SCHEDULE2_LOAD[]
