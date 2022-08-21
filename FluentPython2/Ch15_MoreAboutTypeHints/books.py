#!/usr/bin/env python3


import json
from typing import TypedDict
from typing_extensions import reveal_type

# TypedDict is not a type builder like NamedTuple,
# it serves the purpose of type hint annotations for dictionaries.
# None of this will be type checked at runtime by python itself , it will only be used
# by typechecking tooling like MyPy, Pyright, etc.

class BookDict(TypedDict):
    # Expect ``key: values`` of the specified types:
    isbn: str
    title: str
    authors: list[str]
    pagecount: int


def to_xml(book: BookDict) -> str:
    elements: list[str] = []
    for key, value in book.items():
        if isinstance(value, list):
            elements.extend(
                '<AUTHOR>{}</AUTHOR>'.format(n) for n in value
            )
        else:
            tag = key.upper()
            elements.append(f'<{tag}>{value}</{tag}>')
    xml = '\n\t'.join(elements)
    return f'<BOOK>\n\t{xml}\n</BOOK>'


def from_json(data: str) -> BookDict:
    return json.loads(data)



if __name__ == '__main__':
    from typing import TYPE_CHECKING

    book = BookDict(
        isbn='0134757599',
        title='Refactoring, 2e',
        authors=['Martin Fowler', 'Kent Beck'],
        pagecount=478
    )
    authors = book['authors']
    if TYPE_CHECKING:
        reveal_type(authors)
    # `authors` is expected to be a list[str], but assign just str,
    # type checkers should warn here
    authors = 'Bob'
    # undeclared key
    book['weight'] = 4.2
    del book['title']
