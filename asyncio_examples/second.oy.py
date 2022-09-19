import asyncio


async def test():
    print("test called...")
    await asyncio.sleep(2)
    print("awake..")
    return "done"


async def main():
    print("hi")
    t = (
        test()
    )  # only returns a corounite and does not execute any code present in test methos unless we await it.
    res = None
    print("sleeping in main")
    await asyncio.sleep(1)
    await asyncio.sleep(1)
    print("awake in main")
    res = (
        await t
    )  # the method `test() code` is only called when we await on a coroutine.
    print(f"result: {res}")


if __name__ == "__main__":
    asyncio.run(
        main()
    )  # this will only retunr once the function has completed. # its like await main()
    print("DOne..")
