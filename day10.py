#!/usr/bin/env python
"""AOC 2024 Day 09."""

from typing import Optional, Union

import numpy as np

from aoc import Runner


def load_map(file_name: str) -> np.ndarray:
    """Load the disk block description and generate the disk map."""
    return np.genfromtxt(file_name, dtype=np.byte, ndmin=2, delimiter=1, comments="-")


def find_heads(map: np.ndarray) -> list[tuple[int, int]]:
    """Find all trail head coords in the map."""
    heads = []
    it = np.nditer(map, flags=["multi_index"])
    while not it.finished:
        if it[0] == 0:
            heads.append((it.multi_index[1], it.multi_index[0]))
        it.iternext()
    return heads


def walk_trail(
    map: np.ndarray,
    step: tuple[int, int],
    steps: Optional[set[tuple[int, int]]] = None,
    ratings: bool = False,
) -> Union[set, list]:
    """Walk all trail heads and find a set or list of trail end coords."""
    if steps is None:
        steps = set()
    steps.add(step)

    x_pos, y_pos = step
    altitude = map[y_pos, x_pos]
    y_max, x_max = map.shape
    all_walk_ends = list() if ratings else set()
    for x_dir, y_dir in (
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ):
        next_step = (x_pos + x_dir, y_pos + y_dir)
        x_next, y_next = next_step
        if not (0 <= x_next < x_max and 0 <= y_next < y_max):
            continue

        if (next_step) in steps:
            continue

        altitude_next = map[y_next, x_next]
        if altitude_next != altitude + 1:
            continue

        if altitude_next == 9:
            all_walk_ends.append(next_step) if ratings else all_walk_ends.add(next_step)  # type: ignore
            continue

        next_steps = steps
        if ratings:
            next_steps = steps.copy()
        walk_ends = walk_trail(map, next_step, next_steps, ratings)
        all_walk_ends.extend(walk_ends) if ratings else all_walk_ends.update(walk_ends)  # type: ignore

    return all_walk_ends


def sum_trail_heads(map: np.ndarray) -> int:
    """Find and sum all the trails ends for the heads."""
    heads = find_heads(map)

    return sum([len(walk_trail(map, head)) for head in heads])


def sum_trail_ratings(map: np.ndarray) -> int:
    """Find and sum all the trails ends for the heads."""
    heads = find_heads(map)

    return sum([len(walk_trail(map, head, ratings=True)) for head in heads])


def main() -> None:
    """Day tasks."""
    runner = Runner(
        10,
        sum_trail_heads,
        sum_trail_ratings,
        loader=load_map,
    )
    runner.part_1(36)
    runner.part_2(81)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
