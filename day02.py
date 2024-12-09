#!/usr/bin/env python
"""AOC 2024 Day 02."""

from aoc import Runner


def line_parser(line: str) -> list[int]:
    """Extract data from stripped lines."""
    return [int(val) for val in line.split(" ") if val]


class Checker:
    """Report entry pair checker."""

    def __init__(self) -> None:
        """Ctor."""
        self.direction = None

    def check(self, entry_pair: tuple[int, int]) -> bool:
        """Check a pair of entries."""
        delta = entry_pair[1] - entry_pair[0]

        if delta == 0 or abs(delta) > 3:
            # print(f"{entry_pair=} {delta=}")
            return False

        direction = delta > 0
        if self.direction is None:
            self.direction = direction

        else:
            if self.direction != direction:
                # print(f"{self.direction=} {direction=}")
                return False

        return True


def get_dampened_reports(report: str) -> list[str]:
    """Return a list of reports with a level removed."""
    reports = []
    for idx in range(len(report)):
        dampened_report = report.copy()
        del dampened_report[idx]
        reports.append(dampened_report)

    return reports


def check_reports(
    data: list[str],
    dampened: bool = False,
) -> int:
    """Day 02."""
    safety_count = 0
    dampen_max = 1 if dampened else 0
    for report in data:
        dampen_count = 0
        while dampen_count <= dampen_max:
            # build a list of reports with dampen_count levels removed
            dampened_reports = [report]
            for _ in range(dampen_count):
                tmp_reports = []
                for tmp_report in dampened_reports:
                    tmp_reports.extend(get_dampened_reports(tmp_report))

                dampened_reports = tmp_reports

            dampen_count += 1

            # check reports until a safe one is found
            safe = False
            for dampened_report in dampened_reports:
                checker = Checker()
                checks = map(
                    checker.check,
                    zip(dampened_report, dampened_report[1:], strict=False),
                )
                if all(checks):
                    safety_count += 1
                    safe = True
                    break

            if safe:
                break

    return safety_count


def main() -> None:
    """Day tasks."""
    runner = Runner(
        2,
        check_reports,
        extra_args_2=[True],
        line_parser=line_parser,
    )
    runner.part_1(2)
    runner.part_2(4)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
