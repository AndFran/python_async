import asyncio
import random

work_queue = asyncio.Queue(10)  # limit the size of the queue for testing
producer_finished_event = asyncio.Event()

producer_finished_event.clear()


async def producer():
    """
    producer produce work at variable rate
    """
    for i in range(10):
        await asyncio.sleep(random.randint(1, 4))
        await work_queue.put(i)
    producer_finished_event.set()  # Single no more work


async def consumer():
    while True:
        item = await work_queue.get()  # get some work
        waiting = random.randint(0, 2)

        print(f"processing {item} for {waiting} second(s)")
        await asyncio.sleep(waiting)
        print(f"Finished processing {item}")

        work_queue.task_done()  # set task as done, remove from queue


async def main():
    """
    Basically we have 1 producer task that adds items to an async queue
    and we have n number of consumer tasks that read from the queue and process the data

    We await producer_finished_event to be raised to single the end of the producer work
    We await that the work_queue is empty before exiting the program
    """
    asyncio.create_task(producer())

    [asyncio.create_task(consumer()) for _ in range(5)]  # create a pool of n number of consumers

    await producer_finished_event.wait()
    await work_queue.join()  # wait for this queue to be empty

    print("All work finished")


asyncio.run(main())
