#!/usr/bin/env python
"""AOC 2024 Day 09."""

from functools import cache

from aoc import Runner


def digits(value: int) -> int:
    """Count the digits in a number."""
    digits = 0
    while value > 0:
        digits += 1
        value //= 10
    return digits


@cache
def blink(stone: int, times: int) -> int:
    """Blink at the stones."""
    if times == 0:
        return 1

    if stone == 0:
        return blink(1, times - 1)

    else:
        stone_digits = digits(stone)
        if stone_digits % 2 == 0:
            stone_str = str(stone)
            stone_str_mid = stone_digits // 2
            return blink(
                int(stone_str[:stone_str_mid]),
                times - 1,
            ) + blink(
                int(stone_str[stone_str_mid:]),
                times - 1,
            )

    return blink(stone * 2024, times - 1)


def keep_blinking(stones: list[int], times: int) -> int:
    """Blink a number of times at the stones."""
    return sum([blink(stone, times) for stone in stones])


def main() -> None:
    """Day tasks."""
    runner = Runner(
        11,
        keep_blinking,
        extra_args_1=[25],
        extra_args_2=[75],
        line_parser=lambda line: [int(val) for val in line.split(" ")],
        load_parser=lambda data: data[0],
    )
    runner.part_1(55312)
    runner.part_2()


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
