#!/usr/bin/env python
"""AOC 2024 Day 03."""

import re

from aoc import Runner


def load_data(file_name: str) -> str:
    """Load all the data as a single string."""
    with open(file_name) as file_object:
        return file_object.read()


def cleanse_instructions_1(data: str) -> int:
    """Cleanse and run corrupted instructions 1."""
    instructions = re.findall(r"mul\((?P<lhs>\d+),(?P<rhs>\d+)\)", data, re.M)

    return sum(map(lambda val: int(val[0]) * int(val[1]), instructions))


def cleanse_instructions_2(data: str) -> int:
    """Cleanse and run corrupted instructions 2."""
    matches = re.findall(
        r"(do\(\)|don't\(\)|mul\((?P<lhs>\d+),(?P<rhs>\d+)\))",
        data,
        re.M,
    )

    do = True
    total = 0
    for instruction, lhs, rhs in matches:
        if instruction == "do()":
            do = True

        elif instruction == "don't()":
            do = False

        else:
            if do:
                total += int(lhs) * int(rhs)

    return total


def main() -> None:
    """Day tasks."""
    runner = Runner(
        3,
        cleanse_instructions_1,
        cleanse_instructions_2,
        split_test_data=True,
        loader=load_data,
    )
    runner.part_1(161)
    runner.part_2(48)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
