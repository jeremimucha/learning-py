#!/usr/bin/env python3
import asyncio
import sys
from keyword import kwlist

from domainlib import multi_probe


async def main(tld: str) -> None:
    tld = tld.strip('.')
    # Generate keywords with length up to 4
    names = (kw for kw in kwlist if len(kw) <= 4)
    # Generate domain names with the given suffix as TLD
    domains = (f'{name}.{tld}'.lower() for name in names)
    # Format a header for the tabular output.
    print('FOUND\t\tNOT FOUND')
    print('=====\t\t=========')
    # Asynchronously iterate over `multi_probe(domains)`
    async for domain, found in multi_probe(domains):
        # Set indent to zero or two tabs to put the result in the proper column.
        indent = '' if found else '\t\t'
        print(f'{indent}{domain}')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        # Run the main coroutine with the given command line argument
        asyncio.run(main(sys.argv[1]))
    else:
        print('Please provide a TLD.', f'Example: {sys.argv[0]} COM.BR')
