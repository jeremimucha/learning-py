#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
_ROOT = _SCRIPT.parent
while _ROOT.name != 'PythonConcurrencyWithAsyncio':
    _ROOT = _ROOT.parent
sys.path.append(str(_ROOT))

import asyncio
import concurrent.futures
from concurrent.futures import ProcessPoolExecutor
import functools
from multiprocessing import Value
import time
from typing import Dict, List


# Demonstration of using shared process data.


# Global shared state. Initilized by ProcessPoolExecutor using the init() function
map_progress: Value

# Shared state initializer
def init(progress: Value):
    global map_progress
    map_progress = progress


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)

    # Track number of map updates
    with map_progress.get_lock():
        map_progress.value += 1
    
    return counter


# Report progress every second
async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f'Finished {map_progress.value}/{total_partitions} map operations')
        await asyncio.sleep(1)


# Helper to partition data into smaller chunks of arbitrary size
def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]
    return merged


async def frequencies_async(loop: asyncio.AbstractEventLoop, partition_size: int):
    global map_progress
    
    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        contents = f.readlines()
        # Process only part of the dataset
        contents = contents[:len(contents)//5]
        tasks = []
        start = time.time()

        map_progress = Value('i', 0)
        with concurrent.futures.ProcessPoolExecutor(
                initializer=init, initargs=(map_progress,)) as pool:

            # Run the reporter in this process
            total_partitions = len(contents) // partition_size
            reporter = asyncio.create_task(progress_reporter(total_partitions))

            for chunk in partition(contents, partition_size):
                # For each partition, run the map operation in a separate process.
                # `map_frequencies` mutates `map_progress`
                tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies, chunk)))

            # Wait for all map operations to complete.
            intermediate_results = await asyncio.gather(*tasks)
            # Wait for the reporter coroutine to also finish.
            await reporter

            # Reduce all our intermediate map results into a result
            final_result = functools.reduce(merge_dictionaries, intermediate_results)
            # word, count = next(final_result.items())
            # print(f"{word} has appeared {count} times.)")

            end = time.time()
            print(f'Final map_progress: {map_progress}')
            print(f'Async MapReduce took: {(end - start):.4f} seconds')


async def main():
    loop = asyncio.get_running_loop()
    await frequencies_async(loop, 60000)


if __name__ == '__main__':
    # Issue on Windows - need to use the SelectEventLoopPolicy to avoid `RuntimeError: Event loop is closed`
    if os.name == 'nt':  # Windows
         asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # frequencies_sequential()    # Sequential runtime: 74.6170

    asyncio.run(main())
