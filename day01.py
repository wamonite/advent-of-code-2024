#!/usr/bin/env python
"""AOC 2024 Day 01."""

from collections import Counter

from aoc import load_data


def _get_data(line: str) -> list[int]:
    """Extract data from stripped lines."""
    return [int(val) for val in line.split(" ") if val]


def get_distance(file_name: str, expected: int = None) -> None:
    """Day 01 task 1."""
    data = [_get_data(line) for line in load_data(file_name)]

    columns_sorted = [sorted(col) for col in zip(*data, strict=True)]
    distances = [
        abs(row_pair[0] - row_pair[1]) for row_pair in zip(*columns_sorted, strict=True)
    ]
    distance_sum = sum(distances)
    print(distance_sum)

    if expected is not None:
        assert distance_sum == expected


def get_similarity(file_name: str, expected: int = None) -> None:
    """Day 01 task 2."""
    data = [_get_data(line) for line in load_data(file_name)]

    columns = list(zip(*data, strict=True))
    column_counter_right = Counter(columns[1])
    similarities = [row_idx * column_counter_right[row_idx] for row_idx in columns[0]]
    similarity_sum = sum(similarities)
    print(similarity_sum)

    if expected is not None:
        assert similarity_sum == expected


def main() -> None:
    """Day tasks."""
    get_distance("data/day01.test.txt", 11)
    get_distance("data/day01.txt")
    get_similarity("data/day01.test.txt", 31)
    get_similarity("data/day01.txt")


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, AssertionError):
        pass
