"""
explore2.py: Script to explore the OSCON schedule feed

    >>> import json
    >>> raw_feed = json.load(open('data/osconfeed.json'))
    >>> feed = FrozenJSON(raw_feed)
    >>> len(feed.Schedule.speakers)
    357
    >>> sorted(feed.Schedule.keys())
    ['conferences', 'events', 'speakers', 'venues']
    >>> feed.Schedule.speakers[-1].name
    'Carina C. Zona'
    >>> talk = feed.Schedule.events[40]
    >>> talk.name
    'There *Will* Be Bugs'
    >>> talk.speakers
    [3471, 5199]
    >>> talk.flavor
    Traceback (most recent call last):
      ...
    KeyError: 'flavor'

"""

# tag::EXPLORE2[]
from collections import abc
import keyword

class FrozenJSON:
    """A read-only façade for navigating a JSON-like object
       using attribute notation
    """

    # Calling a class to create an instance first calls the special method __new__.
    # It's a class method, but gets special treatment and isn't decorated with @classmethod.
    # __new__ can implement some logic on construction, possibly returning an instance of
    # a different class (!) - in those cases __init__ isn't called.
    # The construction logic is something like:
    #   def make(cls, *args, **kwargs):
    #       obj = cls.__new__(*args, **kwargs)
    #       if isinstance(obj, cls):
    #           cls.__init__(obj, *args, **kwargs)
    #       return obj
    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            # The default behavior is to delegate to the __new__ of a superclass.
            # In this case we are calling __new__ from the object base class,
            # passing FrozenJSON as the only argument.
            return super().__new__(cls)
        # The remaining lines of __new__ are the same as the build() class method was,
        # i.e. just implement the needed construction logic.
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            # This is where FrozenJSON.build() was called before; noew we just call the FrozenJSON class,
            # which Python handles by calling FrozenJSON.__new__.
            return FrozenJSON(self.__data[name])

    def __dir__(self):
        return self.__data.keys()
# end::EXPLORE2[]
