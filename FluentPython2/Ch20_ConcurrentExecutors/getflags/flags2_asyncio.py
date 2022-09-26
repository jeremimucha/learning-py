#!/usr/bin/env python3

"""Download flags of countries (with error handling).

asyncio async/await version

"""
# tag::FLAGS2_ASYNCIO_TOP[]
import asyncio
from collections import Counter
from http import HTTPStatus
from pathlib import Path

import httpx
import tqdm  # type: ignore

from flags2_common import main, DownloadStatus, save_flag

# low concurrency default to avoid errors from remote site,
# such as 503 - Service Temporarily Unavailable
DEFAULT_CONCUR_REQ = 5
MAX_CONCUR_REQ = 1000

# Very similar to the sequential implementation, however the client is necessary here.
async def get_flag(client: httpx.AsyncClient,
                   base_url: str,
                   cc: str) -> bytes:
    url = f'{base_url}/{cc}/{cc}.gif'.lower()
    # AsyncClient.get() is a coroutine - we await it
    resp = await client.get(url, timeout=3.1, follow_redirects=True)
    resp.raise_for_status()
    return resp.content

async def download_one(client: httpx.AsyncClient,
                       cc: str,
                       base_url: str,
                       semaphore: asyncio.Semaphore,
                       verbose: bool) -> DownloadStatus:
    try:
        # Use an asyncio.semaphore as an async context manager, so that the program
        # as a whole is not blocked. Only this coroutine is suspended when the semaphore
        # counter is zero.
        # __aenter__ .acquire()'s the sempahore, __aexit__ .release()'s it.
        async with semaphore:
            image = await get_flag(client, base_url, cc)
    # Error handling logic is the same as in synchronous code
    except httpx.HTTPStatusError as exc:
        res = exc.response
        if res.status_code == HTTPStatus.NOT_FOUND:
            status = DownloadStatus.NOT_FOUND
            msg = f'not found: {res.url}'
        else:
            raise
    else:
        # save_flag is an I/O operation - to avoid blocking the event loop,
        # run save_flag on a thread.
        await asyncio.to_thread(save_flag, image, f'{cc}.gif')
        # ! The `asyncio.to_thread()` was added in python3.9.           !
        # ! For older pythons use the following:                        !
        # ! loop = asyncio.get_running_loop()                           !
        # ! loop.run_in_executor(None, save_flag, image, f'{cc}.gif')   !
        # Passing `None` as the `executor`` argument to `run_in_executor()`
        # selects the default ThreadPoolExecutor, that is always available
        # in asyncio event loop.
        status = DownloadStatus.OK
        msg = 'OK'
    if verbose and msg:
        print(cc, msg)
    return status
# end::FLAGS2_ASYNCIO_TOP[]


# Takes exactly the same arguments as `download_many`, however
# it can not be invoked directly from main, because it's a coroutine and not a plain function
# like download_many.
async def supervisor(cc_list: list[str],
                     base_url: str,
                     verbose: bool,
                     concur_req: int) -> Counter[DownloadStatus]:
    counter: Counter[DownloadStatus] = Counter()
    # Create an asyncio.Semaphore() that will not allow more than `concur_req`
    # active coroutines among those using this semaphore.
    semaphore = asyncio.Semaphore(concur_req)
    async with httpx.AsyncClient() as client:
        # Create a list of coroutine objects, one per call to the download_one coro.
        to_do = [download_one(client, cc, base_url, semaphore, verbose)
                 for cc in sorted(cc_list)]
        # Get an iterator that will return coroutine objects as they are done.
        to_do_iter = asyncio.as_completed(to_do)
        if not verbose:
            # If not verbose, further wrap the as_completed iterator with the tqdm generator function
            # to display progress.
            to_do_iter = tqdm.tqdm(to_do_iter, total=len(cc_list))
        # Declare and initialize error with None, this will be used to hold an exception
        # beyond the try/except statement if one is raised.
        error: httpx.HTTPError | None = None
        # Iterate over the completed coroutine objects; this loop is similar to the one
        # in download_many
        for coro in to_do_iter:
            try:
                # await on the coro to get its result. This will not block, because
                # as_completed only produces coroutines that are done.
                status = await coro
            except httpx.HTTPStatusError as exc:
                error_msg = 'HTTP error {resp.status_code} - {resp.reason_phrase}'
                error_msg = error_msg.format(resp=exc.response)
                # Preserve the exception for use later.
                error = exc
            except httpx.RequestError as exc:
                error_msg = f'{exc} {type(exc)}'.strip()
                # Preserve the exception for use later.
                error = exc
            except KeyboardInterrupt:
                break

            if error:
                # If there was an error - set the status.
                status = DownloadStatus.ERROR
                if verbose:
                    url = str(error.request.url)  # If verbose - extract the url from exception
                    cc = Path(url).stem.upper()   # and the name of the file to display the country code
                    print(f'{cc} error: {error_msg}')
            counter[status] += 1

    return counter

def download_many(cc_list: list[str],
                  base_url: str,
                  verbose: bool,
                  concur_req: int) -> Counter[DownloadStatus]:
    coro = supervisor(cc_list, base_url, verbose, concur_req)
    # download_many instantiates the supervisor coroutine object and passes it to the event loop,
    # with asyncio.run, collecting the counter supervisor returns when the event loop ends.
    counts = asyncio.run(coro)

    return counts

if __name__ == '__main__':
    main(download_many, DEFAULT_CONCUR_REQ, MAX_CONCUR_REQ)
# end::FLAGS2_ASYNCIO_START[]
