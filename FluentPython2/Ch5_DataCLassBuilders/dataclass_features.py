#!/usr/bin/env python3


from dataclasses import dataclass, field


# Dataclasses protect against constructing classes with members that have mutable defaults,
# which is a common source of bugs:

@dataclass
class ClubMemberWrong:
    name: str
    # The following would result in a ValueError exception
    # guests: list = []

# Instead the following should be used
@dataclass
class ClubMember:
    name: str
    # Use field(default_factory=...) for all mutable types!
    guests: list = field(default_factory=list)


# The `dataclasses.field` function keywords:
# - default - default value for a field
# - default_factory - 0-parameter function used to construct default
# - init - True - include field in params to __init__
# - repr - True - include in __repr__
# - compare - True - use in generated __eq__
# - hash - None - include in generated __hash__ (if requested)
# - metadata - None - mapping with user-defined data

# Initialization
# - generated __init__() only assigns the passed in values or generates the defaults
# - __post_init__() - use to do additional processing on initialization 
