#!/usr/bin/env python
"""AOC 2024 Day 09."""

from itertools import chain, count, repeat
from typing import Iterator

from tqdm import tqdm

from aoc import Runner

FREE_SPACE_ID = -1


def block_generator() -> Iterator[int]:
    """Generate the disk block description file id or the FREE_SPACE_ID."""
    for file_id, free_space_id in zip(count(0), repeat(FREE_SPACE_ID)):
        yield file_id
        yield free_space_id


def map_generator(map: str) -> Iterator[int]:
    """Generate the disk map as a list of ints."""
    return chain.from_iterable(
        [
            int(code) * [file_id]
            for code, file_id in zip(map, block_generator(), strict=False)
        ],
    )


def load_map(file_name: str) -> list[int]:
    """Load the disk block description and generate the disk map."""
    with open(file_name) as file_object:
        block_description = file_object.readline().rstrip()

    return list(map_generator(block_description))


def calculate_checksum(disk_map: list[int]) -> int:
    """Calculate the checksum of the disk map."""
    return sum(
        [
            file_id * idx
            for file_id, idx in zip(disk_map, count(0), strict=False)
            if file_id != FREE_SPACE_ID
        ],
    )


def defrag_blocks(disk_map: list[int]) -> int:
    """Defrag the disk map and calculate the checksum."""
    start = 0
    end = len(disk_map) - 1
    while True:
        while disk_map[end] == FREE_SPACE_ID and start != end:
            end -= 1
        while disk_map[start] != FREE_SPACE_ID and start != end:
            start += 1

        if start == end:
            break

        # swap
        disk_map[start] = disk_map[end]
        disk_map[end] = FREE_SPACE_ID

    return calculate_checksum(disk_map)


def _defrag_file(
    disk_map: list[int],
    end: int,
    file_size: int,
) -> None:
    start = 0
    while True:
        while disk_map[start] != FREE_SPACE_ID and start != end:
            start += 1

        free_space_size = 0
        while (
            disk_map[start + free_space_size] == FREE_SPACE_ID
            and start + free_space_size != end
        ):
            free_space_size += 1

        if start == end:
            break

        if free_space_size >= file_size:
            for idx in range(file_size):
                disk_map[start + idx] = disk_map[end - file_size + idx + 1]
                disk_map[end - file_size + idx + 1] = FREE_SPACE_ID

            return

        start += free_space_size


def defrag_files(disk_map: list[int]) -> int:
    """Defrag the disk map and calculate the checksum."""
    end = len(disk_map) - 1
    with tqdm(total=end) as pbar:
        start = 0
        while True:
            while disk_map[start] != FREE_SPACE_ID and start != end:
                start += 1
                pbar.update()

            while disk_map[end] == FREE_SPACE_ID and start != end:
                end -= 1
                pbar.update()

            file_size = 0
            while disk_map[end - file_size] == disk_map[end] and start != end:
                file_size += 1

            if start == end:
                break

            _defrag_file(disk_map, end, file_size)

            end -= file_size
            pbar.update(file_size)

    return calculate_checksum(disk_map)


def main() -> None:
    """Day tasks."""
    runner = Runner(
        9,
        defrag_blocks,
        defrag_files,
        loader=load_map,
    )
    runner.part_1(1928)
    runner.part_2(2858)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
