#!/usr/bin/env python3


from collections import OrderedDict
from typing import List


def get_creators(record: dict) -> List:
    match record:
        case {'type': 'book', 'api': 2, 'authors': [*names]}:
            return names
        case {'type': 'book', 'api': 1, 'author': name}:
            return [name]
        case {'type': 'book'}:
            raise ValueError(f"Invalid 'book' record: {record!r}")
        case {'type': 'movie', 'director': name}:
            return [name]
        case _:
            raise ValueError(f"Invalid record: {record!r}")


def main():
    b1 = dict(api=1, author='Douglas Hofstadter', type='book', title='Godel, Escher, Bach')
    b1_creators = get_creators(b1)
    print(b1)
    print(b1_creators)

    b2 = OrderedDict(api=2, type='book', title='Python in a Nutshell', authors='Martelli Ravenscroft Holden'.split())
    b2_creators = get_creators(b2)
    print(b2)
    print(b2_creators)


if __name__ == '__main__':
    main()
