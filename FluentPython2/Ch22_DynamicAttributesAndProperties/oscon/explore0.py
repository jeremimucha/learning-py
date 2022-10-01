"""
explore0.py: Script to explore the OSCON schedule feed

# tag::EXPLORE0_DEMO[]
    >>> import json
    >>> raw_feed = json.load(open('data/osconfeed.json'))
    >>> feed = FrozenJSON(raw_feed)  # <1>
    >>> len(feed.Schedule.speakers)  # <2>
    357
    >>> feed.keys()
    dict_keys(['Schedule'])
    >>> sorted(feed.Schedule.keys())  # <3>
    ['conferences', 'events', 'speakers', 'venues']
    >>> for key, value in sorted(feed.Schedule.items()): # <4>
    ...     print(f'{len(value):3} {key}')
    ...
      1 conferences
    484 events
    357 speakers
     53 venues
    >>> feed.Schedule.speakers[-1].name  # <5>
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]
    >>> type(talk)  # <6>
    <class 'explore0.FrozenJSON'>
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers  # <7>
    [3471, 5199]
    >>> talk.flavor  # <8>
    Traceback (most recent call last):
      ...
    KeyError: 'flavor'

# end::EXPLORE0_DEMO[]

"""

# tag::EXPLORE0[]
from collections import abc


class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

    def __init__(self, mapping):
        # Build a dict from the given mapping. This ensures we get a mapping
        # or something that can be converted to one.
        self.__data = dict(mapping)

    # __getattr__ is called only when there's no attribute with that name.
    def __getattr__(self, name):
        try:
            # If name matches an attribute of the instance __data dict, return that.
            # This handles calls like `feed.keys()` - the `keys` method is an attribute
            # of the __data dict.
            return getattr(self.__data, name)
        except AttributeError:
            # Otherwise fetch the item with the key name from self.__data,
            # and return the result of calling FrozenJSON.build() on that.
            return FrozenJSON.build(self.__data[name])

    # Implementing __dir__ supports the dir() built-in, which in turn supports
    # auto completion in the standard Python console as well as IPython.
    # This simple addition supports recursive auto-completion.
    def __dir__(self):
        return self.__data.keys()

    @classmethod
    # This is an alternate constructor - common use for the @classmethod decorator.
    def build(cls, obj):
        # If obj is a mapping - build a FrozenJSON with it.
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        # If it's a MutableSequence it must be a list - build a list,
        # by passing each item in obj recursively to .build()
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        # Otherwise return the item as is.
        else:
            return obj
# end::EXPLORE0[]
