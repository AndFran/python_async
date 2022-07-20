import asyncio
import time
import functools
from typing import Dict
from concurrent.futures import ProcessPoolExecutor

"""
Over engineered multi-process map reduce, should obviously be used for larger data sets than lines, and use chunking etc.
"""


lines = [
    "A long time ago",
    "long ago so long",
    "ago that no one",
    "can remember and no",
    "tree can remember and",
    "no rock can remember",
    "so long ago that",
    "there were no people",
    "and there were no",
    "trees and the rocks",
    "had not been made"
]


def map_text_to_frequency(text: str) -> Dict[str, int]:
    mapped = {}
    words = text.split(' ')
    for word in words:
        word = word.lower()
        mapped[word] = mapped.get(word, 0) + 1
    return mapped


def merge_dicts(first_dict: Dict[str, int], second_dict: Dict[str, int]) -> Dict[str, int]:
    final = first_dict.copy()  # dont modify the original
    for key in second_dict:
        final[key] = final.get(key, 0) + second_dict[key]
    return final


async def main():
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    start = time.perf_counter()

    all_tasks = []

    with ProcessPoolExecutor() as pool:
        for line in lines:
            all_tasks.append(loop.run_in_executor(pool, functools.partial(map_text_to_frequency, line)))

        mapping_results = await asyncio.gather(*all_tasks)

    final = functools.reduce(merge_dicts, mapping_results)
    print(final)

    print(f"Duration {time.perf_counter() - start}")


if __name__ == '__main__':
    asyncio.run(main())
