#!/usr/bin/env python3

from pathlib import Path
import sys
import os
_SCRIPT = Path(__file__).parent.resolve()
while _ROOT := _SCRIPT.parent:
    if _ROOT.name == 'PythonConcurrencyWithAsyncio': break
sys.path.append(str(_ROOT))

import asyncio
import concurrent.futures
import functools
import time
from typing import Dict, List


def frequencies_sequential():
    freqs = {}

    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        lines = f.readlines()

        start = time.time()

        for line in lines:
            data = line.split('\t')
            word = data[0]
            count = int(data[2])
            if word in freqs:
                freqs[word] += count
            else:
                freqs[word] = count
        
        end = time.time()
        print(f'Sequential runtime: {end-start:.4f}')


# Helper to partition data into smaller chunks of arbitrary size
def partition(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]


def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)
    return counter


def merge_dictionaries(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            merged[key] += second[key]
        else:
            merged[key] = second[key]
    return merged


async def reduce(loop: asyncio.AbstractEventLoop, pool, counters, chunk_size) -> Dict[str, int]:
    # Partition the dictionaries into parallelizable chunks
    chunks: List[List[Dict]] = list(partition(counters, chunk_size))
    reducers = []

    while len(chunks[0]) > 1:
        for chunk in chunks:
            # Reduce each partition into a single dictionary
            reducer = functools.partial(functools.reduce, merge_dictionaries, chunk)
            reducers.append(loop.run_in_executor(pool, reducer))
        
        # Wait for all reduce operations to complete
        reducer_chunks = await asyncio.gather(*reducers)
        # Partition the results again, and start a new iteration of the loop.
        chunks = list(partition(reducer_chunks, chunk_size))
        reducers.clear()

    return chunks[0][0]


async def frequencies_async(loop: asyncio.AbstractEventLoop, partition_size: int):
    with open('googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        contents = f.readlines()
        # Process only part of the dataset
        contents = contents[:len(contents)//10]
        tasks = []
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as pool:
            for chunk in partition(contents, partition_size):
                # For each partition, run the map operation in a separate process
                tasks.append(loop.run_in_executor(pool, functools.partial(map_frequencies, chunk)))

                # Wait for all map operations to complete.
            intermediate_results = await asyncio.gather(*tasks)

            # Reduce all our intermediate map results into a result
            # final_result = functools.reduce(merge_dictionaries, intermediate_results)
            
            # Parallelize the reduce operation
            final_result = await reduce(loop, pool, intermediate_results, 500)
            # word, count = next(final_result.items())
            # print(f"{word} has appeared {count} times.)")

            end = time.time()
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
