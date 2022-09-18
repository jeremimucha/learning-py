#!/usr/bin/env python3


from concurrent import futures

from flags import save_flag, get_flag, main


def download_one(cc: str) -> str:
    image = get_flag(cc)
    save_flag(image, f'{cc}.gif')
    print(cc, end=' ', flush=True)
    return cc



# The `executor.submit(callable, args)` and `futures.as_completed(futures)` combination
# is more flexible than `executor.map()` - map is designed to run the same calalble on
# different arguments, where as with `.submit()` we can pass different callables
# and arguments, and futures passed to `.as_completed()` may come from more than one
# executor - possibly with some futures comming from a ThreadPoolExecutor and others
# from ProcessPoolExecutor.

def download_many(cc_list: list[str]) -> int:
    cc_list = cc_list[:5]
    # with futures.ThreadPoolExecutor() as executor:
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        todo: list[futures.Future] = []
        for cc in sorted(cc_list):
            future = executor.submit(download_one, cc)
            todo.append(future)
            print(f'Scheduled for {cc}: {future}')

        for count, future in enumerate(futures.as_completed(todo), 1):
            res: str = future.result()
            print(f'{future} result: {res!r}')
    
    return count

    # The above is equivalent to the implementation from `flags_threadpool`,
    # aside for some differences like max_workers count.
    # Here, we get to inspect how the Futures work.
    # First we submit the task to the executor, which returns a Future object.
    # futuers.as_completed() is a generator which yields futures as they complete.

    # with futures.ThreadPoolExecutor() as executor:
    #     res = executor.map(download_one, sorted(cc_list))
    
    # return len(list(res))


if __name__ == '__main__':
    main(download_many)
