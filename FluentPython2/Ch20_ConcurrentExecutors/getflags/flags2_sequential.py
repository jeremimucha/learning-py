#!/usr/bin/env python3

"""Download flags of countries (with error handling).

Sequential version

Sample run::

    $ python3 flags2_sequential.py -s DELAY b
    DELAY site: http://localhost:8002/flags
    Searching for 26 flags: from BA to BZ
    1 concurrent connection will be used.
    --------------------
    17 flags downloaded.
    9 not found.
    Elapsed time: 13.36s

"""

# tag::FLAGS2_BASIC_HTTP_FUNCTIONS[]
from collections import Counter
from http import HTTPStatus

import httpx
import tqdm  # type: ignore  # <1>

from flags2_common import main, save_flag, DownloadStatus  # <2>

DEFAULT_CONCUR_REQ = 1
MAX_CONCUR_REQ = 1

def get_flag(base_url: str, cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    resp = httpx.get(url, timeout=3.1, follow_redirects=True)
    # `.raise_for_status()` raises HttpStatusError if the HTTP status code is not in range(200, 300)
    resp.raise_for_status()
    return resp.content

def download_one(cc: str, base_url: str, verbose: bool = False) -> DownloadStatus:
    try:
        image = get_flag(base_url, cc)
    except httpx.HTTPStatusError as exc:
        # Handle 404 specifically...
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            # by setting its local status to DownloadStatus.NOT_FOUND
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            # Re-raise any other exception to propagate to the caller
            raise
    else:
        save_flag(image, f'{cc}.gif')
        status = DownloadStatus.OK
        msg = 'OK'

    if verbose:
        # Display country code and status message is verbose output has been requested.
        print(cc, msg)

    return status
# end::FLAGS2_BASIC_HTTP_FUNCTIONS[]

# tag::FLAGS2_DOWNLOAD_MANY_SEQUENTIAL[]
def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  _unused_concur_req: int) -> Counter[DownloadStatus]:
    # Keep a tally of the different download outcomes
    counter: Counter[DownloadStatus] = Counter()
    cc_iter = sorted(cc_list)   # sort the input list of country codes
    if not verbose:
        # If not output verbose, animate the progress bar
        cc_iter = tqdm.tqdm(cc_iter)
    for cc in cc_iter:
        try:
            # Make sequential calls to download_one()
            status = download_one(cc, base_url, verbose)
        # Handle any errors not handled by download_one()
        except httpx.HTTPStatusError as exc:
            error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
            error_msg = error_msg.format(resp=exc.response)
        # network-related exceptions
        except httpx.RequestError as exc:
            error_msg = f'{exc} {type(exc)}'.strip()
        # Ctrl-C
        except KeyboardInterrupt:
            break
        # if no exceptions
        else:
            error_msg = ''

        if error_msg:
            status = DownloadStatus.ERROR
        counter[status] += 1
        if verbose and error_msg:
            print(f'{cc} error: {error_msg}')

    return counter  # <12>
# end::FLAGS2_DOWNLOAD_MANY_SEQUENTIAL[]

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
