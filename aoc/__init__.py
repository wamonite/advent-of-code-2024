"""Advent of Code 2024 utility functions."""

import time
from typing import Any, Callable, Optional


def load_data(file_name: str, line_parser: Optional[Callable[[str], str]]) -> list[str]:
    """Load lines from a file and strip line ends."""
    with open(file_name) as file_object:
        return [
            line_parser(line.rstrip()) if line_parser else line.rstrip()
            for line in file_object.readlines()
        ]


class Runner:
    """Test runner."""

    def __init__(
        self,
        day: int,
        function_1: Callable[[Any], Any],
        function_2: Optional[Callable[[Any], Any]] = None,
        *,
        split_test_data: bool = False,
        split_data: bool = False,
        extra_args_1: Optional[list[Any]] = None,
        extra_args_2: Optional[list[Any]] = None,
        loader: Optional[Callable[[str], Any]] = None,
        line_parser: Optional[Callable[[str], str]] = None,
        load_parser: Optional[Callable[[list[str]], Any]] = None,
    ) -> None:
        """
        Run, test and output in a consistent manner.

        day - day number
        function_1 - function for part 1
        function_2 - (optional) function for part 2
        split_test_data - use different test data for parts (test1.txt and test2.txt)
        split_data - use different data for parts (1.txt and 2.txt)
        extra_args_1 - (optional) list of extra arguments to call function with
        extra_args_2 - (optional) list of extra arguments to call function with
        loader - (optional) function loads data from a file name
        line_parser - (optional) function that parses data from each line in the file
        load_parser - (optional) function that parses data from all lines in the file

        line_parser and load_parser are unused if loader is provided
        """
        self.day = day
        self.function = (function_1, function_2 if function_2 else function_1)
        self.file_name: dict[str, tuple[str, str]] = {}
        self.file_name["test"] = (
            f"data/day{day:02d}.test1.txt"
            if split_test_data
            else f"data/day{day:02d}.test.txt",
            f"data/day{day:02d}.test2.txt"
            if split_test_data
            else f"data/day{day:02d}.test.txt",
        )
        self.file_name["proper"] = (
            f"data/day{day:02d}.1.txt" if split_data else f"data/day{day:02d}.txt",
            f"data/day{day:02d}.2.txt" if split_data else f"data/day{day:02d}.txt",
        )
        self.extra_args = (extra_args_1, extra_args_2)
        self.loader = loader
        self.line_parser = line_parser
        self.load_parser = load_parser

    def _run(
        self,
        part_one: bool = True,
        expected: Optional[int] = None,
    ) -> None:
        part = 0 if part_one else 1
        test = expected is not None
        name = f"{self.day:02d}-{part + 1}"
        file_name = self.file_name["test" if test else "proper"][part]

        if self.loader:
            data = self.loader(file_name)
        else:
            data = load_data(file_name, self.line_parser)
            if self.load_parser:
                data = self.load_parser(data)

        print(f"#### {name} ", end="")
        start_time = time.time()
        function = self.function[part]
        extra_args = self.extra_args[part]
        result = function(data, *extra_args) if extra_args else function(data)
        time_elapsed = time.time() - start_time
        expected_str = f" {expected=}" if expected else ""
        print(f"time={time_elapsed*1000:.2f}ms{expected_str} {result=}")
        if expected is not None:
            if result != expected:
                print(f"!!!! {result} != {expected}")
                raise RuntimeError

    def _part(
        self,
        part_one: bool = True,
        expected: Optional[int] = None,
    ) -> None:
        self._run(part_one, expected)
        self._run(part_one)

    def part_1(self, expected: Optional[int] = None) -> None:
        """Run part 1 tasks."""
        self._part(True, expected)

    def part_2(self, expected: Optional[int] = None) -> None:
        """Run part 2 tasks."""
        self._part(False, expected)
