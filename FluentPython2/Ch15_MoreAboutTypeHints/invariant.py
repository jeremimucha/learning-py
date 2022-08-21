#!/usr/bin/env python3


# Invariant types - accept only the type specified, neither types from
#   up or down the inheritance hierarchy are accepted.
# Covariant types - accepts types from ``down`` the inheritance hierarchy.
#   Those are generally return types. E.g. in C++ a virtual clone() function
#   would return a pointer to a base type.
# Contravariant types - accept types from ``up`` the inheritance hierarchy.
#   Those would be input parameters. E.g. in C++ a parameter to a function,
#   accepting a `Foo const&` would also accept the classes Foo derives from.


from typing import TypeVar, Generic


class Beverage:
    """Any beverage."""

class Juice(Beverage):
    """Any fruit juice."""

class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""


T = TypeVar('T')

class BeverageDispenser(Generic[T]):
    """A dispenser parameterized on the beverage type."""
    def __init__(self, beverage: T) -> None:
        self.beverage = beverage

    def dispense(self) -> T:
        return self.beverage


# Use a generic constrained with a specific type
def install(dispenser: BeverageDispenser[Juice]) -> None:
    """Install a fuir juice dispenser."""


if __name__ == '__main__':
    # The problem is that the `install` declaration as written right now,
    # is too strict - it accepts only `Juice`, but wouldn't accept
    # types derived from `Juice`
    
    juice_dispenser = BeverageDispenser(Juice())
    install(juice_dispenser)    # all good, typechecker approves

    # Illegal:
    beverage_disp = BeverageDispenser(Beverage())
    install(beverage_disp)      # type checker complains - incompatible type

    # But this is also illegal:
    oj_dispenser = BeverageDispenser(OrangeJuice())
    install(oj_dispenser)   # incompatible type!

    # see covariant.py for followup
