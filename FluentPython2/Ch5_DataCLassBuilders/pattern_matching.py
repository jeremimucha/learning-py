#!/usr/bin/env python3

import typing


class City(typing.NamedTuple):
    continent: str
    name: str
    country: str


cities = [
    City('Asia', 'Tokyo', 'JP'),
    City('Asia', 'Delhi', 'IN'),
    City('North America', 'Mexico City', 'MX'),
    City('North America', 'New York', 'US'),
    City('South America', 'São Paulo', 'BR'),
]


# Matching can be done by keyword:
def match_asian_cities():
    results = []
    for city in cities:
        match city:
            case City(continent='Asia'):
                results.append(city)
    return results


def match_asian_countries():
    results = []
    for city in cities:
        match city:
            case City(continue='Asia', country=cc):
                results.append(cc)
    return results


# Matching can also be done positionally:
def match_asian_cities_pos():
    results = []
    for city in cities:
        match city:
            case City("Asia"):
                results.append(city)
    return results


def match_asian_countries_pos():
    results = []
    for city in cities:
        match city:
            case City('Asia', _, country):
                results.append(country)
    return results
