#!/usr/bin/env python
"""AOC 2024."""

from dataclasses import dataclass, field
from itertools import count
from typing import Self

from aoc import Runner


@dataclass(frozen=True)
class SideCoordinate:
    """Side coordinates."""

    x: int
    y: int
    horizontal: bool
    left_or_above: bool


@dataclass
class Plot:
    """Plot."""

    id: int
    block: str
    area: int = 0
    side_coords: set[SideCoordinate] = field(default_factory=set)

    def __eq__(self, other: Self) -> bool:  # type: ignore
        """Check equality on id."""
        return self.id == other.id

    def merge(self, other: Self) -> None:
        """Merge a plot into another."""
        self.area += other.area
        self.side_coords.update(other.side_coords)

    @property
    def perimeter(self) -> int:
        """Return the perimeter."""
        return len(self.side_coords)

    @property
    def sides(self) -> int:
        """Return the number of sides."""
        side_coords = self.side_coords.copy()
        side_count = 0
        while side_coords:
            side_count += 1
            coord = side_coords.pop()

            for iter in count(1, 1), count(-1, -1):
                for idx in iter:
                    coord_new = (
                        SideCoordinate(
                            coord.x + idx,
                            coord.y,
                            True,
                            coord.left_or_above,
                        )
                        if coord.horizontal
                        else SideCoordinate(
                            coord.x,
                            coord.y + idx,
                            False,
                            coord.left_or_above,
                        )
                    )
                    if coord_new in side_coords:
                        side_coords.remove(coord_new)

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
            plot.side_coords.add(SideCoordinate(0, self.row_idx, False, False))

        else:
            plot_left = self.row_plots[-2]
            if plot != plot_left:
                plot.side_coords.add(
                    SideCoordinate(col_idx, self.row_idx, False, True),
                )
                plot_left.side_coords.add(
                    SideCoordinate(col_idx, self.row_idx, False, False),
                )

            if col_idx == self.width - 1:
                plot.side_coords.add(
                    SideCoordinate(self.width, self.row_idx, False, True),
                )

        # above
        if self.row_plots_last:
            plot_above = self.row_plots_last[col_idx]
            if block == plot_above.block:
                if plot != plot_above:
                    self._merge_plot(plot_above, plot)

        plot = self.row_plots[-1]
        if self.row_idx == 0:
            plot.side_coords.add(SideCoordinate(col_idx, 0, True, True))

        else:
            plot_above = self.row_plots_last[col_idx]
            if plot != plot_above:
                plot.side_coords.add(
                    SideCoordinate(col_idx, self.row_idx, True, True),
                )
                plot_above.side_coords.add(
                    SideCoordinate(col_idx, self.row_idx, True, False),
                )

            if self.row_idx == self.height - 1:
                plot.side_coords.add(SideCoordinate(col_idx, self.height, True, False))

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
    # for map in [
    #     [
    #         "EEEEE",
    #         "EXXXX",
    #         "EEEEE",
    #         "EXXXX",
    #         "EEEEE",
    #     ],
    #     [
    #         "AAAAAA",
    #         "AAABBA",
    #         "AAABBA",
    #         "ABBAAA",
    #         "ABBAAA",
    #         "AAAAAA",
    #     ],
    # ]:
    #     calc = MapCalculator(len(map[0]), len(map), False)
    #     for row in map:
    #         calc.calculate_row(row)
    #     print(calc.cost())
    #     for plot in calc.plot_lookup.values():
    #         print(f"{plot.id=} {plot.block=} {plot.sides=}")

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
