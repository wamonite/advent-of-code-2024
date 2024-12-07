#!/usr/bin/env python
"""AOC 2024 Day 01."""

from collections import Counter

from aoc import runner


def line_parser(line: str) -> list[int]:
    """Extract data from stripped lines."""
    return [int(val) for val in line.split(" ") if val]


def get_distance(data: list[list[int]]) -> int:
    """Day 01 task 1."""
    columns_sorted = [sorted(col) for col in zip(*data, strict=True)]
    distances = [
        abs(row_pair[0] - row_pair[1]) for row_pair in zip(*columns_sorted, strict=True)
    ]
    return sum(distances)


def get_similarity(data: list[list[int]]) -> int:
    """Day 01 task 2."""
    columns = list(zip(*data, strict=True))
    column_counter_right = Counter(columns[1])
    similarities = [row_idx * column_counter_right[row_idx] for row_idx in columns[0]]
    return sum(similarities)


def main() -> None:
    """Day tasks."""
    runner(
        "01-1",
        "data/day01.test.txt",
        get_distance,
        line_parser=line_parser,
        expected=11,
    )
    runner(
        "01-1",
        "data/day01.txt",
        get_distance,
        line_parser=line_parser,
    )
    runner(
        "01-2",
        "data/day01.test.txt",
        get_similarity,
        line_parser=line_parser,
        expected=31,
    )
    runner(
        "01-2",
        "data/day01.txt",
        get_similarity,
        line_parser=line_parser,
    )


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
