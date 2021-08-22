#! /usr/bin/env python

import asyncio
import urllib.parse
import sys


# Simple exapmle querying HTTP(S) headers of the URL passed on the command line


async def print_http_headers(url):
    url = urllib.parse.urlsplit(url)
    port, ssl = (443, True) if url.scheme == 'https' else (80, False)
    reader, writer = await asyncio.open_connection(url.hostname, port, ssl=ssl)

    query = (
        f"HEAD {url.path or '/'} HTTP/1.0\r\n"
        f"Host: {url.hostname}\r\n"
        f"\r\n"
    )

    writer.write(query.encode('latin-1'))
    while True:
        line = await reader.readline()
        if not line:
            break

        line = line.decode('latin1').rstrip()
        if line:
            print(f"HTTP header> {line}")

    # Ignore the body, close the socket
    writer.close()


if __name__ == '__main__':
    url = sys.argv[1]
    asyncio.run(print_http_headers(url))
