"""Advent of Code 2024 utility functions."""

import time
from typing import Any, Callable, Optional


def load_data(file_name: str, line_parser: Optional[Callable]) -> list[str]:
    """Load lines from a file and strip line ends."""
    with open(file_name) as file_object:
        data = [line.rstrip() for line in file_object.readlines()]
    return [line_parser(line) for line in data] if line_parser else data


def runner(
    name: str,
    file_name: str,
    function: Callable,
    *,
    extra_args: Optional[list[Any]] = None,
    loader: Callable = load_data,
    line_parser: Optional[Callable] = None,
    expected: Optional[Any] = None,
) -> None:
    """Run, test and output in a consistent manner."""
    print(f"#### {name} ", end="")
    data = loader(file_name, line_parser)
    start_time = time.time()
    result = function(data, *extra_args) if extra_args else function(data)
    time_elapsed = time.time() - start_time
    expected_str = f" {expected=}" if expected else ""
    print(f"time={time_elapsed*1000:.2f}ms{expected_str} {result=}")
    if expected is not None:
        if result != expected:
            print(f"!!!! {result} != {expected}")
            raise RuntimeError
