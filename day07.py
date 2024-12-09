#!/usr/bin/env python
"""AOC 2024 Day 07."""

from operator import add, mul
from typing import Callable

from tqdm import tqdm

from aoc import Runner


def line_parser(line: str) -> list[int]:
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
    data: list[int],
    operators: list[Callable],
) -> int:
    """Sum all the target numbers that can be calculated."""
    return sum(
        [
            line[0] if calculate(line[0], line[1], line[2:], operators) else 0
            for line in tqdm(data)
        ],
    )


def main() -> None:
    """Day tasks."""
    operators_part1 = [add, mul]
    operators_part2 = [add, mul, lambda lhs, rhs: int(str(lhs) + str(rhs))]

    runner = Runner(
        7,
        calibrate,
        extra_args_1=[operators_part1],
        extra_args_2=[operators_part2],
        line_parser=line_parser,
    )
    runner.part_1(3749)
    runner.part_2(11387)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
