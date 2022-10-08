#!/usr/bin/env python3


from typing import Protocol, runtime_checkable, Any

@runtime_checkable
class RandomPicker(Protocol):
    def pick(self) -> Any: ...


if __name__ == '__main__':
    pass
