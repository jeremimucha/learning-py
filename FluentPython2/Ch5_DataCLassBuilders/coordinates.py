#!/usr/bin/env python3


# Lots of boilerplate,
# No meaningful __repr__
# No meaningful comparison
class CoordinateRaw:
    def __init__(self, lat, lon) -> None:
        self.lat = lat
        self.lon = lon


from typing import NamedTuple

# NamedTuple is really a metaclass here
# Coordinate is a subclass of plain `tuple` here
# Features:
# - immutable instances
# - ._asdict()
# - ._fields
# - ._field_defaults
# - .__annotations__
# - ._replace(...)  - new instance with changes
# - NamedTuple(...) - new class at runtime
class CoordinateNamedTuple(NamedTuple):
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f"{abs(self.lat):.1f}*{ns}, {abs(self.lon):.1f}*{we}"


from dataclasses import dataclass
# Features:
# - mutable instances
# - dataclasses.asdict(x)
# - [f.name for f in datacalsses.fields(x)]
# - [f.default for f in dataclasses.fields(x)]
# - x.__annotations__
# - dataclasses.replace(x, ...) - new instance with changes
# - dataclasses.make_dataclass(...) - new class at runtime
@dataclass(frozen=True) # frozen=True makes instances immutable
class CoordinateDataClass:
    lat: float
    lon: float

    def __str__(self):
        ns = 'N' if self.lat >= 0 else 'S'
        we = 'E' if self.lon >= 0 else 'W'
        return f"{abs(self.lat):.1f}*{ns}, {abs(self.lon):.1f}*{we}"

