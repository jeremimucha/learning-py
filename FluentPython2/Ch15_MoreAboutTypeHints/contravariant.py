#!/usr/bin/env python3


# Contravariant - types from up the hierarchy are accepted



# * Refuse is the most general type of trash. All trash is refuse.
# * Biodegradable is a specific type of trash that can be decom‐
#   posed by organisms over time. Some Refuse is not Biodegradable.
# * Compostable is a specific type of Biodegradable trash that can
#   be efficiently turned into organic fertilizer in a compost bin or
#   in a composting facility. Not all Biodegradable trash is Compo
#   stable in our definition.

from typing import TypeVar, Generic


class Refuse:
    """Any refuse."""

class Biodegradeable(Refuse):
    """Biodegradeable refuse."""

class Compostable(Biodegradeable):
    """Compostable refuse"""


# Contravariant type declaration
T_contra = TypeVar('T_contra', contravariant=True)

class TrashCan(Generic[T_contra]):
    def put(self, refuse: T_contra) -> None:
        """Store trash until dumped."""


def deploy(trash_can: TrashCan[Biodegradeable]):
    """Deploy a trash can for biodegradeable refuse."""



if __name__ == '__main__':
    bio_can: TrashCan[Biodegradeable] = TrashCan()
    deploy(bio_can) # All good

    # Still good, `Refuse` trashcan can take more types of
    # trash than a biodegradeable trash can
    trash_can: TrashCan[Refuse] = TrashCan()
    deploy(trash_can)

    # Not acceptable - Compostable is more strict than Biodegradeable
    compost_can: TrashCan[Compostable] = TrashCan()
    deploy(compost_can)
