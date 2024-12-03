#!/usr/bin/env python
"""AOC 2024 Day 03."""

import re


def cleanse_instructions_1(file_name: str, expected: int = None) -> None:
    """Cleanse and run corrupted instructions 1."""
    with open(file_name) as file_object:
        data = file_object.read()

    instructions = re.findall(r"mul\((?P<lhs>\d+),(?P<rhs>\d+)\)", data, re.M)

    total = sum(map(lambda val: int(val[0]) * int(val[1]), instructions))

    print(total)

    if expected is not None:
        assert total == expected


def cleanse_instructions_2(file_name: str, expected: int = None) -> None:
    """Cleanse and run corrupted instructions 2."""
    with open(file_name) as file_object:
        data = file_object.read()

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

    print(total)

    if expected is not None:
        assert total == expected


def main() -> None:
    """Day tasks."""
    cleanse_instructions_1("data/day03.test1.txt", expected=161)
    cleanse_instructions_1("data/day03.txt")
    cleanse_instructions_2("data/day03.test2.txt", expected=48)
    cleanse_instructions_2("data/day03.txt")


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, AssertionError):
        pass
