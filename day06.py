#!/usr/bin/env python
"""AOC 2024 Day 06."""

import numpy as np

GUARD_DIR = [
    (0, 1),
    (-1, 0),
    (0, -1),
    (1, 0),
]
GUARD_CHARS = "v<^>"


def load_map(file_name: str) -> tuple[list[list[str]], tuple[int, int], int]:
    """Load the map and find the guard."""
    map = np.genfromtxt(file_name, dtype="U1", ndmin=2, delimiter=1, comments="-")

    y_max, x_max = map.shape
    for y_pos in range(y_max):
        for x_pos in range(x_max):
            guard_char = map[y_pos, x_pos]
            if guard_char in GUARD_CHARS:
                return map, (x_pos, y_pos), GUARD_CHARS.index(guard_char)


def out_of_bounds(pos: tuple[int, int], size: tuple[int, int]) -> bool:
    """Check if the position out of the bounds of the map."""
    x_pos, y_pos = pos
    x_max, y_max = size
    return x_pos < 0 or x_pos >= x_max or y_pos < 0 or y_pos >= y_max


def get_next_guard_pos(
    map: np.ndarray,
    guard_pos: tuple[int, int],
    guard_dir: int,
) -> tuple[tuple[int, int], int]:
    """Find the next position and direction of the guard."""
    y_max, x_max = map.shape
    for _ in range(4):
        x_dir, y_dir = GUARD_DIR[guard_dir]
        x_pos, y_pos = guard_pos
        x_pos += x_dir
        y_pos += y_dir

        # print(f"{guard_pos=} {x_dir=} {y_dir=} {x_pos=} {y_pos=}")
        if out_of_bounds((x_pos, y_pos), (x_max, y_max)):
            return None, None

        if map[y_pos, x_pos] != "#":
            return (x_pos, y_pos), guard_dir

        guard_dir += 1
        if guard_dir == len(GUARD_DIR):
            guard_dir = 0


def count_guard_steps(file_name: str, expected: int = None) -> None:
    """Count how many locations explored before the guard leaves the map."""
    map, guard_pos, guard_dir = load_map(file_name)

    pos_set = set()
    while True:
        pos_set.add(guard_pos)

        guard_pos, guard_dir = get_next_guard_pos(map, guard_pos, guard_dir)
        if guard_pos is None:
            break

    total = len(pos_set)
    print(total)

    if expected is not None:
        assert total == expected


def count_guard_loops(file_name: str, expected: int = None) -> None:
    """Count how many times adding an obstruction puts the guard in a loop."""
    map, guard_pos_init, guard_dir_init = load_map(file_name)

    total = 0
    y_max, x_max = map.shape
    for y_pos in range(y_max):
        for x_pos in range(x_max):
            if map[y_pos, x_pos] != ".":
                continue

            # set the obstruction
            map[y_pos, x_pos] = "#"

            # reset the guard
            guard_pos = guard_pos_init
            guard_dir = guard_dir_init

            pos_set = set()
            while True:
                pos_set.add((guard_pos, guard_dir))

                guard_pos, guard_dir = get_next_guard_pos(map, guard_pos, guard_dir)

                # are we off the map?
                if guard_pos is None:
                    break

                # are we in a loop?
                if (guard_pos, guard_dir) in pos_set:
                    total += 1
                    break

            # reset the obstruction
            map[y_pos, x_pos] = "."

    print(total)

    if expected is not None:
        assert total == expected


def main() -> None:
    """Day tasks."""
    count_guard_steps("data/day06.test.txt", expected=41)
    count_guard_steps("data/day06.txt")
    count_guard_loops("data/day06.test.txt", expected=6)
    count_guard_loops("data/day06.txt")


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, AssertionError):
        pass
