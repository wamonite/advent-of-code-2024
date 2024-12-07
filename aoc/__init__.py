"""Advent of Code 2024 utility functions."""

import time
from typing import Any, Callable, Optional


def load_data(file_name: str, line_parser: Optional[Callable]) -> list[str]:
    """Load lines from a file and strip line ends."""
    with open(file_name) as file_object:
        return [
            line_parser(line.rstrip()) if line_parser else line.rstrip()
            for line in file_object.readlines()
        ]


def runner(
    name: str,
    file_name: str,
    function: Callable,
    *,
    extra_args: Optional[list[Any]] = None,
    loader: Optional[Callable] = None,
    line_parser: Optional[Callable] = None,
    load_parser: Optional[Callable] = None,
    expected: Optional[Any] = None,
) -> None:
    """
    Run, test and output in a consistent manner.

    name - display name
    file_name - file to load
    function - function under test
    extra_args - list of extra arguments to call function with
    loader - (optional) function loads data from a file name
    line_parser - (optional) function that parses data from each line in the file
    load_parser - (optional) function that parses data from all lines in the file
    expected - value that the function return value is compared against

    line_parser and load_parser are unused if loader is provided
    """
    if loader:
        data = loader(file_name) if loader else load_data(file_name, line_parser)
    else:
        data = load_data(file_name, line_parser)
        if load_parser:
            data = load_parser(data)

    print(f"#### {name} ", end="")
    start_time = time.time()
    result = function(data, *extra_args) if extra_args else function(data)
    time_elapsed = time.time() - start_time
    expected_str = f" {expected=}" if expected else ""
    print(f"time={time_elapsed*1000:.2f}ms{expected_str} {result=}")
    if expected is not None:
        if result != expected:
            print(f"!!!! {result} != {expected}")
            raise RuntimeError
