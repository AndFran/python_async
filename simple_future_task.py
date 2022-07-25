import asyncio


def start_long_request() -> asyncio.Future:
    """
    returns a future that has been added to a task which will
    complete in the future, callers do not know we use a task for this
    """
    future = asyncio.Future()
    asyncio.create_task(long_task(future))
    return future


async def long_task(future: asyncio.Future) -> None:
    """
    Models the actual processing task
    """
    await asyncio.sleep(2)
    future.set_result("The answer")


async def main():
    future = start_long_request()

    result = await future

    print(result)


asyncio.run(main())


