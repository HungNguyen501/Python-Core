"""One billion row challenge https://github.com/gunnarmorling/1brc"""
from multiprocessing import Pool, cpu_count
import argparse
import logging
import logging.config
import os
import time

logging.config.fileConfig(fname="configs/logging.cfg")
logger = logging.getLogger(__name__)


def get_chunk_files(file_path: int, process_num: int = 8):
    """Calculate indies of file chunks that include start index and end index"""
    file_size = os.path.getsize(filename=file_path)
    chunk_size = file_size // process_num
    chunks = []
    with open(file=file_path, mode="r+b") as fopen:
        chunk_start = 0
        while chunk_start < file_size:
            chunk_end = temp_end = min(file_size, chunk_start + chunk_size)
            fopen.seek(chunk_end)
            while chunk_start <= chunk_end < file_size and fopen.read(1) != b"\n":
                chunk_end -= 1
                fopen.seek(chunk_end)
            if chunk_end == chunk_start:
                fopen.seek(temp_end)
                while fopen.read(1) != b"\n":
                    temp_end += 1
                    fopen.seek(temp_end)
                chunk_end = temp_end
            chunk_end += 1
            chunks.append((file_path, chunk_start, chunk_end,))
            chunk_start = chunk_end
    return chunks


# pylint: disable=R1730
def handle_file_chunk(file_path: str, start: int, end: str):
    """Calculcate statistics of a file chunk"""
    with open(file=file_path, mode="r+b") as fopen:
        fopen.seek(start)
        result = {}
        buffer_size = 1024 * 1024
        byte_count = end - start
        remain = b""
        location = None
        while byte_count > 0:
            if buffer_size > byte_count:
                buffer_size = byte_count
            byte_count -= buffer_size
            buffer = remain + fopen.read(buffer_size)
            index = 0
            while buffer:
                if not location:
                    try:
                        semicolon = buffer.index(b";", index)
                        location = buffer[index:semicolon]
                    except ValueError:
                        remain = buffer[index:]
                        break
                    index = semicolon + 1
                try:
                    new_line = buffer.index(b"\n", index)
                except ValueError:
                    remain = buffer[index:]
                    break
                temperature = float(buffer[index:new_line])
                index = new_line + 1
                try:
                    if temperature < result[location][0]:
                        result[location][0] = temperature
                    elif temperature > result[location][1]:
                        result[location][1] = temperature
                    result[location][2] += temperature
                    result[location][3] += 1
                except KeyError:
                    result[location] = [temperature, temperature, temperature, 1]
                location = None
    return result


def main():
    """Run main program"""
    parser = argparse.ArgumentParser(description="Run calculate_one_billion_row_challenge")
    parser.add_argument("-f", "--file", help="Input file path", required=True)
    args = vars(parser.parse_args())
    file_path = args["file"]
    logger.info("File: %s", file_path)
    max_cpu = min(8, cpu_count())
    logger.info(f"Number of processes: {max_cpu}")
    start_time = time.time()
    chunks = get_chunk_files(file_path=file_path, process_num=max_cpu)
    with Pool(processes=max_cpu) as pool:
        chunk_results = pool.starmap(func=handle_file_chunk, iterable=chunks,)
    score = {}
    stat_locations = {}
    for chunk in chunk_results:
        for location, stats in chunk.items():
            if location not in stat_locations:
                stat_locations[location] = stats
            else:
                if stat_locations[location][0] > stats[0]:
                    stat_locations[location][0] = stats[0]
                if stat_locations[location][1] < stats[1]:
                    stat_locations[location][1] = stats[1]
                stat_locations[location][2] += stats[2]
                stat_locations[location][3] += stats[3]
    for location, stats in stat_locations.items():
        score[location.decode()] = (round(stats[0], 1), round(stats[2] / stats[3], 1), round(stats[1], 1),)
    # logger.info(score)
    logger.info("Run time: %f", time.time() - start_time)


if __name__ == "__main__":
    main()
