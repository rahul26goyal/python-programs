import asyncio
import random


async def count_task():
    """
    An async task with print  something and async waits for sometime to
    :return:
    """
    rand = random.randint(1, 10)
    print(f"One: {rand}")
    await asyncio.sleep(1)  # could be any async call which can be awaited.
    print(f"Two: {rand}")
    return rand


async def start_async_tasks():
    # executing multiple task concurrently.
    # using the `gather` API to execute all the tasks without waiting for each one to complete.
    # but the await is only returned when all tasks are completed.
    result = await asyncio.gather(count_task(),
                         count_task(),
                         count_task(),
                         count_task()
                         )
    print(f"completed executing all tasks....: {result}")


def main():
    import time
    start = time.perf_counter()
    asyncio.run(start_async_tasks())
    elapsed = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed} seconds")


if __name__ == '__main__':
    main()
