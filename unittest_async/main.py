"""Execute fetch events asynchonously"""
import time
from functools import cache
import json
import subprocess
import random
import asyncio
from aiohttp import ClientSession
import aiofiles


@cache
def read_data(file_path: str) -> str:
    """Cache data from file to avoid IO

    Args:
        file_path(str): path of file

    Returns file content as str
    """
    with open(file=file_path, mode="r", encoding="utf-8") as fi:
        return fi.read()


# pylint: disable=W0613
async def fetch_event(session: ClientSession, event_id: str):
    """Fetch event by its id"""
    sleep_time = random.choice([6, 7, 8, 9, 10])
    print(f"{event_id}: sleep in {sleep_time} seconds")
    await asyncio.sleep(sleep_time)
    try:
        return json.loads(s=read_data(file_path="./data/fictional_events.json"))[event_id]
    except KeyError:
        return {event_id: "event_id not found"}


async def write_outputs(
    output_file_path: str, session: ClientSession,
    event_id: str, semaphore_config: asyncio.Semaphore
):
    """Write output to file"""
    result = await fetch_event(session=session, event_id=event_id)
    async with semaphore_config:
        async with aiofiles.open(file=output_file_path, mode="a") as fo:
            await fo.write(str(result) + "\n")


async def main(output_file: str, li_events: list[str]):
    """Execute main program"""
    subprocess.run(args=["rm", "-rf", output_file], check=True)
    # Limit of file descriptors in OS to prevent OSError: [Errno 24] Too many open files
    # Read more in https://wilsonmar.github.io/maximum-limits/
    num_of_max_files_open = 10000
    semaphore_config = asyncio.Semaphore(value=num_of_max_files_open)
    async with ClientSession() as session:
        tasks = [
            write_outputs(
                output_file_path=output_file,
                session=session, event_id=i,
                semaphore_config=semaphore_config
            )
            for i in li_events
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main=main(
        output_file="./data/output.txt",
        li_events=[str(i) for i in range(10000)]
    ))
    print(f"Execution time: {time.time() - start_time}")
