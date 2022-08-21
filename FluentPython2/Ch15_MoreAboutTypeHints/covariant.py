#!/usr/bin/env python3


# Covariant - types down the hierarchy are accepted


from typing import TypeVar, Generic


class Beverage:
    """Any beverage."""

class Juice(Beverage):
    """Any fruit juice."""

class OrangeJuice(Juice):
    """Delicious juice from Brazilian oranges."""



# covariant type declaration. The _co suffix is conventional.
T_co = TypeVar('T_co', covariant=True)

class BeverageDispenser(Generic[T_co]):
    """A dispenser parameterized on the beverage type."""
    def __init__(self, beverage: T_co) -> None:
        self.beverage = beverage

    def dispense(self) -> T_co:
        return self.beverage


# Use a generic constrained with a specific type
def install(dispenser: BeverageDispenser[Juice]) -> None:
    """Install a fuir juice dispenser."""



if __name__ == '__main__':
    juice_dispenser = BeverageDispenser(Juice())
    install(juice_dispenser)    # all good, typechecker approves

    # This is now valid
    oj_dispenser = BeverageDispenser(OrangeJuice())
    install(oj_dispenser)   # all good


    # Still illegal:
    beverage_disp = BeverageDispenser(Beverage())
    install(beverage_disp)      # type checker complains - incompatible type

