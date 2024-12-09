#!/usr/bin/env python
"""AOC 2024 Day 08."""

from dataclasses import dataclass
from itertools import chain, combinations
from typing import Iterator, Self

import numpy as np

from aoc import Runner


@dataclass(frozen=True)
class Coordinate:
    """Coordinate data with utility methods."""

    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        """Coordinate addition."""
        return Coordinate(
            self.x + other.x,
            self.y + other.y,
        )

    def __sub__(self, other: Self) -> Self:
        """Coordinate subtraction."""
        return Coordinate(
            self.x - other.x,
            self.y - other.y,
        )

    def within(self, limit: Self) -> bool:
        """Check if coordinate is within a coordinate limit."""
        return 0 <= self.x < limit.x and 0 <= self.y < limit.y


def load_map(file_name: str) -> tuple[dict[str, Coordinate], Coordinate]:
    """Load the map and find the antennas."""
    map = np.genfromtxt(file_name, dtype="U1", ndmin=2, delimiter=1, comments="-")

    antenna_to_coord_lookup = {}
    y_max, x_max = map.shape
    for y_pos in range(y_max):
        for x_pos in range(x_max):
            val = str(map[y_pos, x_pos])
            if val != ".":
                coord_set = antenna_to_coord_lookup.setdefault(val, set())
                coord_set.add(Coordinate(x_pos, y_pos))

    return antenna_to_coord_lookup, Coordinate(x_max, y_max)


def count_antinodes(data: tuple[dict[str, Coordinate], Coordinate]) -> int:
    """Count all generated antinodes."""
    antenna_to_coord_lookup, map_limit = data

    antenna_coord_pairs = {
        antenna_coord_pair
        for antenna_coords in antenna_to_coord_lookup.values()
        for antenna_coord_pair in combinations(antenna_coords, 2)
    }
    antinodes = {
        antinode
        for antenna_coord_pair in antenna_coord_pairs
        for antinode in [
            antenna_coord_pair[0] - (antenna_coord_pair[1] - antenna_coord_pair[0]),
            antenna_coord_pair[1] + (antenna_coord_pair[1] - antenna_coord_pair[0]),
        ]
        if antinode.within(map_limit)
    }
    return len(antinodes)


def harmonic_generator(
    antenna_1: Coordinate,
    antenna_2: Coordinate,
    map_limit: Coordinate,
) -> Iterator[Coordinate]:
    """For two antennas yield all antinodes from 1 to 2 including 2 within the map."""
    coord_step = antenna_2 - antenna_1
    coord = antenna_2
    while coord.within(map_limit):
        yield coord
        coord += coord_step


def count_antinodes_including_harmonics(
    data: tuple[dict[str, Coordinate], Coordinate],
) -> int:
    """Count all generated antinodes."""
    antenna_to_coord_lookup, map_limit = data

    antenna_coord_pairs = {
        antenna_coord_pair
        for antenna_coords in antenna_to_coord_lookup.values()
        for antenna_coord_pair in combinations(antenna_coords, 2)
    }
    antinodes = {
        antinode
        for antenna_coord_pair in antenna_coord_pairs
        for antinode in chain(
            harmonic_generator(antenna_coord_pair[0], antenna_coord_pair[1], map_limit),
            harmonic_generator(antenna_coord_pair[1], antenna_coord_pair[0], map_limit),
        )
    }
    return len(antinodes)


def main() -> None:
    """Day tasks."""
    runner = Runner(
        8,
        count_antinodes,
        count_antinodes_including_harmonics,
        loader=load_map,
    )
    runner.part_1(14)
    runner.part_2(34)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
