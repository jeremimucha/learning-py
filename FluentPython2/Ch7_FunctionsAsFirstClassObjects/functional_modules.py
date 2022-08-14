#!/usr/bin/env python3

# There are multiple modules in python that help with writing functional-style code.

from dataclasses import dataclass
from functools import reduce, partial
import functools
from operator import mul, itemgetter, attrgetter, methodcaller
import unicodedata


def factorial(n):
    return reduce(mul, range(1, n+1))


# --- itemgetter

metro_data = [
('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
('São Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]

def print_cities():
    # itemgetter uses operator[], meaning that it
    # supports sequences, mappings and any class implementing __getitem__.
    for city in sorted(metro_data, key=itemgetter(1)):
        print(city)


# --- attrgetter

@dataclass
class LatLon:
    lat: float
    lon: float

@dataclass
class Metropolis:
    name: str
    cc: str
    pop: float
    coord: LatLon

metro_areas = [Metropolis(name, cc, pop, LatLon(lat, lon))
               for name, cc, pop, (lat, lon) in metro_data]

def print_metro_areas():
    """Prints metro-area cities sorted by lattitude"""
    name_lat = attrgetter('name', 'coord.lat')
    for city in sorted(metro_areas, key=attrgetter('coord.lat')):
        print(name_lat(city))



# --- methodcaller
# operator.methodcaller is used to call the named method on objects.
# It can also do partial function application.

def demo_methodcaller():
    s = "The time has come"
    upcase = methodcaller('upper')  # calls obj.upper() on given objects.
    print(upcase(s))
    hyphenate = methodcaller('replace', ' ', '-')
    print(hyphenate(s))



# --- partial
# partial function application

def demo_partial():
    triple = partial(mul, 3)
    print(triple(7))
    list(map(triple, range(1, 10)))

    nfc = partial(unicodedata.normalize, 'NFC')
    s1 = 'cafe\u0301'
    s2 = 'cafe'
    print(s1, s2)
    print(s1 == s2)
    print(nfc(s1) == nfc(s2))
