#!/usr/bin/env python3
"""
``HackerClubMember`` objects accept an optional ``handle`` argument.
If ``handle`` is omitted, it's set to the first part of the member's name.
Handles must be unique. If a handle is already takes another equal handle
will not be generated, instead ValueError is raised.
"""
from dataclasses import InitVar, dataclass, field
from typing import ClassVar, Set

@dataclass
class ClubMember:
    name: str
    guests: list = field(default_factory=list)


@dataclass
class HackerClubMember(ClubMember):
    all_handles = set()     # class attribute
    handle: str = ''        # instance field of type `str` with default value, making it optional

    def __post_init__(self):
        cls = self.__class__
        if self.handle == '':
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:
            msg = f"Handle {self.handle!r} already exists."
            raise ValueError(msg)
        cls.all_handles.add(self.handle)



# When a variable is needed only for initialization, but does not
# become a member data field afterwards, it needs to be type-annotated
# appropriately:
class DatabaseType: pass

@dataclass
class C:
    i: int  # regular member data field
    j: int = None   # member data field with default
    # If we want to declare a typed class data member we need to use
    # ClassVar, otherwise any typed members become instance data fields.
    someclassvar: ClassVar[Set[str]] = set()
    # Variable used only for initialization, does not become a member data field.
    # notice that `ClassVar` comes from `typing`
    # but `InitVar` comes from `dataclasses`... (sigh)
    database: InitVar[DatabaseType] = None

    def __post_init__(self, database):
        # Use, but don't store database
        if self.j is None and database is not None:
            self.j = database.lookup('j')

my_database = DatabaseType()
c = C(10, database=my_database)
