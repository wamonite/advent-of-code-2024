#!/usr/bin/env python
"""AOC 2024 Day 04."""

import numpy as np

XMAS_SEARCH_DIR = (
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
)
X_MAS_SEARCH_DIR = (
    (1, 1),
    (-1, 1),
    (-1, -1),
    (1, -1),
)


def find_xmas(
    data: np.ndarray,
    xpos: int,
    ypos: int,
    xdir: int,
    ydir: int,
) -> bool:
    """Find the word XMAS at xpos, ypos in the direction xdir, ydir."""
    if xdir < 0 and xpos < 3:
        return False
    if ydir < 0 and ypos < 3:
        return False

    ymax, xmax = data.shape
    if xdir > 0 and xpos > xmax - 4:
        return False
    if ydir > 0 and ypos > ymax - 4:
        return False

    for search_char in "XMAS":
        # print(f"{xpos=} {ypos=} {search_char=} {data[xpos][ypos]=}")
        if search_char != data[ypos][xpos]:
            return False

        xpos += xdir
        ypos += ydir

    return True


def count_xmas(data: np.ndarray, xpos: int, ypos: int) -> int:
    """Count all instances of XMAS found at xpos, ypos."""
    total = 0
    for xdir, ydir in XMAS_SEARCH_DIR:
        if find_xmas(data, xpos, ypos, xdir, ydir):
            total += 1

    return total


def find_x_mas(
    data: np.ndarray,
    xpos: int,
    ypos: int,
    xdir: int,
    ydir: int,
) -> bool:
    """Find the word MAS centred at xpos, ypos in the direction xdir, ydir."""
    if xpos < 1:
        return False
    if ypos < 1:
        return False

    ymax, xmax = data.shape
    if xpos > xmax - 2:
        return False
    if ypos > ymax - 2:
        return False

    # could do check MAS then SAM but it's quick enough without needing to
    xpos -= xdir
    ypos -= ydir
    for search_char in "MAS":
        if search_char != data[ypos][xpos]:
            return False

        xpos += xdir
        ypos += ydir

    return True


def count_x_mas(data: np.ndarray, xpos: int, ypos: int) -> int:
    """Return 1 if at least 2 instances of MAS found centred at xpos, ypos."""
    total = 0
    for xdir, ydir in X_MAS_SEARCH_DIR:
        if find_x_mas(data, xpos, ypos, xdir, ydir):
            total += 1
            if total > 1:
                # print(f"{xpos=} {ypos=}")
                return 1

    return 0


def word_search(file_name: str, part_one: bool = True, expected: int = None) -> None:
    """Run the word searches."""
    data = np.genfromtxt(file_name, dtype="U1", ndmin=2, delimiter=1)

    count_func = count_xmas if part_one else count_x_mas
    total = 0
    for ypos in range(data.shape[0]):
        for xpos in range(data.shape[1]):
            total += count_func(data, xpos, ypos)

    print(total)

    if expected is not None:
        assert total == expected


def main() -> None:
    """Day tasks."""
    word_search("data/day04.test.txt", expected=18)
    word_search("data/day04.txt")
    word_search("data/day04.test.txt", part_one=False, expected=9)
    word_search("data/day04.txt", part_one=False)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, AssertionError):
        pass
