#!/usr/bin/env python3


from concurrent import futures

from flags import save_flag, get_flag, main


def download_one(cc: str) -> str:
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc


def download_many(cc_list: list[str]) -> int:
    with futures.ThreadPoolExecutor() as executor:
        # executor.map() maps a callable over an iterable,
        # it returns a generator, that yields values returned by each function call.
        res = executor.map(download_one, sorted(cc_list))
    
    # Constructing a list from the results implicitly checks for errors,
    # as the iterator returned by executor.map(...) will raise an exception,
    # when next() is called, trying to retrieve a result from a failed operation.
    return len(list(res))


if __name__ == '__main__':
    main(download_many)
