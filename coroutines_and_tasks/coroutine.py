import asyncio
import time

async def task(index, n):
    # time.sleep(sleep_time)
    for i in range(n):
        count = 0
        while count < 10000000:
            count += 1
        print(f"task{index}: {i+1}")
        await asyncio.sleep(1)
    print(f"task{index} is done")

async def main1():
    start_time = time.time()

    await asyncio.gather(task(1, 5), task(2, 6), task(3, 3))

    # await fetch_users(1)
    # await fetch_posts(2)

    print(f"finished in  {(time.time() - start_time) :.2f} seconds")

async def main2():
    start_time = time.time()
    
    t1 = asyncio.create_task(task(1, 6))
    t2 = asyncio.create_task(task(2, 5))
    t3 = asyncio.create_task(task(3, 4))

    await t1
    await t2
    await t3

    print(f"finished in  {(time.time() - start_time) :.2f} seconds")

loop = asyncio.get_event_loop()
loop.run_until_complete(main1())

# asyncio.run(main2())





