#!/usr/bin/env python3


# Example of thow to extend static typing protocols:
# - derive from the protocol you intend to extend,
# - derive from typing.Protocol,
# - if the new protocol needs to be runtime_checkable,
#   it needs to be decorated as such again,


from typing import Protocol, runtime_checkable
from randompick import RandomPicker


@runtime_checkable
class LoadableRandomPicker(RandomPicker, Protocol):
    def load(self, Iterable) -> None: ...




if __name__ == '__main__':
    pass
