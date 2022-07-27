from time import perf_counter
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial


def do_long_cpu_task(cycles: int) -> int:
    start = perf_counter()
    for _ in range(0, cycles):
        pass
    end = perf_counter()
    print(f"Finished processing to {cycles} in {end - start}")
    return cycles


async def main():
    with ProcessPoolExecutor() as p_pool:
        loop = asyncio.get_event_loop()

        futures = []

        funcs = [partial(do_long_cpu_task, 100000),
                 partial(do_long_cpu_task, 1000000),
                 partial(do_long_cpu_task, 10000000),
                 partial(do_long_cpu_task, 100000000)]

        for func in funcs:
            futures.append(loop.run_in_executor(executor=p_pool, func=func))

        results = await asyncio.gather(*futures)
        print(results)


if __name__ == '__main__':
    asyncio.run(main())
