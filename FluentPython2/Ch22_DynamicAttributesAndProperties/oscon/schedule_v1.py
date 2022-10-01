"""
schedule_v1.py: traversing OSCON schedule data

# tag::SCHEDULE1_DEMO[]
    >>> records = load(JSON_PATH)  # <1>
    >>> speaker = records['speaker.3471']  # <2>
    >>> speaker  # <3>
    <Record serial=3471>
    >>> speaker.name, speaker.twitter  # <4>
    ('Anna Martelli Ravenscroft', 'annaraven')

# end::SCHEDULE1_DEMO[]

"""

# tag::SCHEDULE1[]
import json

JSON_PATH = 'data/osconfeed.json'

class Record:
    def __init__(self, **kwargs):
        # Common shortcut to build an instance with attributes created from keyword arguments.
        # __dict__ stores attributes of an instance (unless __slots__ is declared), so updating
        # the mapping is a quick way to create a bunch of attributes in that instance.
        self.__dict__.update(kwargs)

    def __repr__(self):
        # Use the `serial` field to build the custom Record representation
        return f'<{self.__class__.__name__} serial={self.serial!r}>'

def load(path=JSON_PATH):
    # load will ultimately return a dict of Record instances.
    records = {}
    with open(path) as fp:
        # Parse the JSON, returning native Python objects: lists, dicts, strings, numbers, etc.
        raw_data = json.load(fp)
    # Iterate over the four top-level lists named 'conferences', 'events', 'speakers' and 'venues'.
    for collection, raw_records in raw_data['Schedule'].items():
        # `record_type` is the list name without the last character, so `speakers` becomes
        # `speaker`. In Python3.9 we can do this more explicitly with `collection.removesuffix('s')`.
        record_type = collection[:-1]
        for raw_record in raw_records:
            # Build the key in the format `speaker.3471`
            key = f'{record_type}.{raw_record["serial"]}'
            # Create a Record and save it in rcords with the key
            records[key] = Record(**raw_record)
    return records
# end::SCHEDULE1[]
