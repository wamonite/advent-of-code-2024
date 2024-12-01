"""Advent of Code 2024 utility functions."""


def load_data(file_name: str) -> list[str]:
    """Load lines from a file and strip line ends."""
    with open(file_name) as file_object:
        return [line.rstrip() for line in file_object.readlines()]
