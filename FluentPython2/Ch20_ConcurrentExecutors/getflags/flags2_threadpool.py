#!/usr/bin/env python3

"""Download flags of countries (with error handling).

ThreadPool version

Sample run::

    $ python3 flags2_threadpool.py -s ERROR -e
    ERROR site: http://localhost:8003/flags
    Searching for 676 flags: from AA to ZZ
    30 concurrent connections will be used.
    --------------------
    150 flags downloaded.
    361 not found.
    165 errors.
    Elapsed time: 7.46s

"""

# tag::FLAGS2_THREADPOOL[]
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus
from flags2_sequential import download_one  # reuse from sequential code

DEFAULT_CONCUR_REQ = 30  # if -m/--max_req has not been specified use this value
MAX_CONCUR_REQ = 1000  # Max number of concurrent downloads, regardless of the value of -m/--max_req


def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    # Create the executor
    with ThreadPoolExecutor(max_workers=concur_req) as executor:
        to_do_map = {}  # Map each Future instance to the country code for reporting.
        for cc in sorted(cc_list):  # Iterate over country codes in alphabetical order.
            # Schedule the download
            future = executor.submit(download_one, cc,
                                     base_url, verbose)
            # Map the future to the country code
            to_do_map[future] = cc
        done_iter = as_completed(to_do_map)  # Get a generator that yields futures as each task is done.
        if not verbose:
            # If not verbose draw the progress bar, `done_iter` has no length, so we need to specify
            # the total explicitly.
            done_iter = tqdm.tqdm(done_iter, total=len(cc_list))
        for future in done_iter:  # Iterate over the futures as they complete
            try:
                status = future.result()  # Get the result. Any potential exceptions will be re-raised here.
            except httpx.HTTPStatusError as exc:  # Exception handling more or less the same as in sequential code.
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
            except KeyboardInterrupt:
                break
            else:
                error_msg = ''

            if error_msg:
                status = DownloadStatus.ERROR
            counter[status] += 1
            if verbose and error_msg:
                cc = to_do_map[future]  # <14>
                print(f'{cc} error: {error_msg}')

    return counter


if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
# end::FLAGS2_THREADPOOL[]
