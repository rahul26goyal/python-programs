import asyncio
import os
import random
import time


async def makeitem(size):
    "Generates random size bytes and returns a hex string"
    return os.urandom(size).hex()


async def produce(producer_name: int, shared_queue: asyncio.Queue):
    num_items = random.randint(1, 5)
    print(f"Producer-{producer_name} will add {num_items} items to Queue.")
    for i in range(0, num_items):
        await asyncio.sleep(random.randint(0, 2))
        item = await makeitem(i + 3)
        await shared_queue.put((i, item, time.perf_counter()))
        print(f"Producer-{producer_name} added <{item}> to queue.")
    return num_items


async def consumer_task(name: int, q: asyncio.Queue):
    print(f"Consumer-{name} is going to start processing..")
    while True:  # this will keep running forevern until cancelled
        p_name, item, insert_time = await q.get()
        print(f"Processing item {item} from producer {p_name}")
        await asyncio.sleep(random.randint(0, 3))
        now = time.perf_counter()
        print(f"Consumer {name} processed task <{item}>"
              f" in {now - insert_time:0.5f} seconds.")
        q.task_done()  # since we are waiting on the  my_queue.join() we need to make task_completed.


async def main():
    print("Generating Producers...")
    my_queue = asyncio.Queue()
    num_producers = 1
    # Create producers
    producers = []
    for p in range(num_producers):
        ptask = asyncio.create_task(produce(p, my_queue))
        producers.append(ptask)
    print(f"Generated producers: {producers}")

    # create consumers now.
    num_consumers = 1
    consumers = []

    for c in range(num_consumers):
        ctask = asyncio.create_task(consumer_task(c, my_queue))
        consumers.append(ctask)
    print(f"Generated consuers: {consumers}")

    items_generated = await asyncio.gather(*producers)
    produced_count = 0
    for i in items_generated:
        produced_count += i
    print(f"done producing all items..: {produced_count}")
    print(f"Queue size: {my_queue.qsize()}")
    await my_queue.join()
    print(f"Queue size: {my_queue.qsize()}")

    print(f"Number of running tasks: {len(asyncio.all_tasks())}")
    for c in consumers:
        c.cancel()
    await asyncio.sleep(5)
    print(f"Number of running tasks: {asyncio.all_tasks()}")


if __name__ == '__main__':
    asyncio.run(main())  # this will only retunr once the function has completed. # its like await main()
    print("DOne..")
