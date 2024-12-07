#!/usr/bin/env python
"""AOC 2024 Day 07."""

from operator import add, mul
from typing import Callable, Optional

from aoc import load_data


def parse_line(line: str) -> list[int]:
    """Return the data as lists of ints."""
    return [int(val[:-1] if val.endswith(":") else val) for val in line.split(" ")]


def calculate(
    target: int,
    first: int,
    values: list[int],
    operators: list[Callable],
) -> bool:
    """Recursively calculate the combinations depth first."""
    # print(f"{target=} {first=} {values=}")
    for op in operators:
        result = op(first, values[0])

        if len(values) == 1:
            # print(f"{target=} {result=}")
            if result == target:
                return True

        else:
            if calculate(target, result, values[1:], operators):
                return True

    return False


def calibrate(
    file_name: str,
    operators: list[Callable],
    expected: Optional[int] = None,
) -> None:
    """Sum all the target numbers that can be calculated."""
    data = [parse_line(line) for line in load_data(file_name)]

    total = sum(
        [
            line[0] if calculate(line[0], line[1], line[2:], operators) else 0
            for line in data
        ],
    )

    print(total)

    if expected is not None:
        assert total == expected


def main() -> None:
    """Day tasks."""
    operators_day1 = [
        add,
        mul,
    ]
    operators_day2 = [add, mul, lambda lhs, rhs: int(str(lhs) + str(rhs))]

    calibrate("data/day07.test.txt", operators_day1, expected=3749)
    calibrate("data/day07.txt", operators_day1)
    calibrate("data/day07.test.txt", operators_day2, expected=11387)
    calibrate("data/day07.txt", operators_day2)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, AssertionError):
        pass
