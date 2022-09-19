import asyncio


async def task(a):
    print(f"Doing task: {a}")
    await asyncio.sleep(1)
    print(f"Done with task: {a}")
    return a


async def main():
    print("running main")
    t1 = asyncio.create_task(
        task("rahul")
    )  # this will return a AsyncTask object and start executing it.
    t2 = asyncio.create_task(task("goyal"))
    print(f"t1: {t1}:::t2:{t2}")
    print("waiting for the tasks to complete")
    result = await asyncio.gather(
        t1, t2
    )  # without this wait the eventloop will not waiti fro t1 and t2 to complete and exit.
    print(f"DOne with all task as listed: {result}")


if __name__ == "__main__":
    asyncio.run(
        main()
    )  # this will only retunr once the function has completed. # its like await main()
    print("DOne..")
