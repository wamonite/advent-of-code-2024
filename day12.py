#!/usr/bin/env python
"""AOC 2024."""

from dataclasses import dataclass, field
from itertools import count
from typing import Self

from aoc import Runner


@dataclass
class Plot:
    """Plot."""

    id: int
    block: str
    area: int = 0
    horizontal_sides: set[tuple[int, int]] = field(default_factory=set)
    vertical_sides: set[tuple[int, int]] = field(default_factory=set)

    def __eq__(self, other: Self) -> bool:  # type: ignore
        """Check equality on id."""
        return self.id == other.id

    def merge(self, other: Self) -> None:
        """Merge a plot into another."""
        self.area += other.area
        self.horizontal_sides.update(other.horizontal_sides)
        self.vertical_sides.update(other.vertical_sides)

    @property
    def perimeter(self) -> int:
        """Return the perimeter."""
        return len(self.horizontal_sides) + len(self.vertical_sides)

    @property
    def sides(self) -> int:
        """Return the number of sides."""
        return self._count_sides(True) + self._count_sides(False)

    def _count_sides(self, horizontal: bool) -> int:
        sides = (
            self.horizontal_sides.copy() if horizontal else self.vertical_sides.copy()
        )
        side_count = 0
        while sides:
            side_count += 1
            coord = sides.pop()

            for iter in count(1, 1), count(-1, -1):
                for idx in iter:
                    coord_new = (
                        (coord[0] + idx, coord[1])
                        if horizontal
                        else (coord[0], coord[1] + idx)
                    )
                    if coord_new in sides:
                        sides.remove(coord_new)

                    else:
                        break

        return side_count


class MapCalculator:
    """Calculate costs for the map."""

    def __init__(self, width: int, height: int, part_one: bool = True) -> None:
        """Ctor."""
        self.width = width
        self.height = height
        self.part_one = part_one
        self.row_idx = 0
        self.plot_id = 0
        self.plot_lookup: dict[int, Plot] = {}
        self.row_plots: list[Plot] = []
        self.row_plots_last: list[Plot] = []

    def _create_plot(self, block: str) -> None:
        plot = Plot(self.plot_id, block)
        self.plot_lookup[self.plot_id] = plot
        self._append_plot(plot)
        self.plot_id += 1

    def _append_plot(self, plot: Plot) -> None:
        self.row_plots.append(plot)
        plot.area += 1

    def _merge_plot(self, new_plot: Plot, old_plot: Plot) -> None:
        # replaces plots in current rows
        self.row_plots_last = [
            new_plot if plot == old_plot else plot for plot in self.row_plots_last
        ]
        self.row_plots = [
            new_plot if plot == old_plot else plot for plot in self.row_plots
        ]
        new_plot.merge(old_plot)
        del self.plot_lookup[old_plot.id]

    def _add_row_block(self, col_idx: int, block: str) -> None:
        # left
        if self.row_plots:
            plot_left = self.row_plots[-1]
            if block == plot_left.block:
                self._append_plot(plot_left)
            else:
                self._create_plot(block)

        else:
            self._create_plot(block)

        plot = self.row_plots[-1]
        if col_idx == 0:
            plot.vertical_sides.add((0, self.row_idx))

        else:
            plot_left = self.row_plots[-2]
            if plot != plot_left:
                plot.vertical_sides.add((col_idx, self.row_idx))
                plot_left.vertical_sides.add((col_idx, self.row_idx))

            if col_idx == self.width - 1:
                plot.vertical_sides.add((self.width, self.row_idx))

        # above
        if self.row_plots_last:
            plot_above = self.row_plots_last[col_idx]
            if block == plot_above.block:
                if plot != plot_above:
                    self._merge_plot(plot_above, plot)

        plot = self.row_plots[-1]
        if self.row_idx == 0:
            plot.horizontal_sides.add((col_idx, 0))

        else:
            plot_above = self.row_plots_last[col_idx]
            if plot != plot_above:
                plot.horizontal_sides.add((col_idx, self.row_idx))
                plot_above.horizontal_sides.add((col_idx, self.row_idx))

            if self.row_idx == self.height - 1:
                plot.horizontal_sides.add((col_idx, self.height))

    def calculate_row(self, row: str) -> None:
        """Update the map calculations from another row."""
        self.row_plots = []
        for idx, block in enumerate(row):
            self._add_row_block(idx, block)

        self.row_idx += 1

        self.row_plots_last = self.row_plots

    def cost(self) -> int:
        """Return the calculated cost."""
        return sum(
            [
                plot.area * (plot.perimeter if self.part_one else plot.sides)
                for plot in self.plot_lookup.values()
            ],
        )


def calculate_map(map: list[str], part_one: bool = True) -> int:
    """Calculate the cost of the map."""
    calc = MapCalculator(len(map[0]), len(map), part_one)

    # print()
    for row in map:
        calc.calculate_row(row)
        # print(" ".join([f"{plot.id}:{plot.block}" for plot in calc.row_plots]))

    # for _, plot in calc.plot_lookup.items():
    #     multiplier = plot.area if calc.part_one else plot.sides
    #     print(f"{plot.block} {plot.area} * {multiplier}")

    return calc.cost()


def main() -> None:
    """Day tasks."""
    runner = Runner(
        12,
        calculate_map,
        extra_args_2=[False],
    )
    runner.part_1(1930)
    runner.part_2(1206)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
