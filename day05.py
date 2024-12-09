#!/usr/bin/env python
"""AOC 2024 Day 05."""

from aoc import Runner


def load_parser(data: list[str]) -> tuple[dict[int, list[int]], list[list[int]]]:
    """Extract the rules and page updates from the file."""
    rules = {}
    updates = []
    for line in data:
        if "|" in line:
            page_l, page_r = line.split("|")
            rule = rules.setdefault(int(page_r), [])
            rule.append(int(page_l))

        elif "," in line:
            updates.append([int(val) for val in line.split(",")])

    return rules, updates


def check_update(rules: dict[int, list[int]], update: list[int]) -> bool:
    """Recursively check the update against the rules returning the result."""
    if len(update) == 1:
        return True

    rule_key = update[0]
    if rule_key in rules:
        rule = rules[rule_key]
        for page in update:
            # print(f"{rule_key=} {rule=} {page=} result={page in rule}")
            if page in rule:
                return False

    return check_update(rules, update[1:])


def fix_update(rules: dict[int, list[int]], update: list[int]) -> list[int]:
    """Recursively fix the update according to the rules and return it."""
    # print(f"{update=}")
    if len(update) == 1:
        return update

    rule_key = update[0]
    if rule_key in rules:
        rule = rules[rule_key]
        for page in update:
            # print(f"{rule_key=} {rule=} {page=} result={page in rule}")
            if page in rule:
                update.remove(page)
                return fix_update(rules, [page] + update)

    return [rule_key] + fix_update(rules, update[1:])


def check_page_order(
    data: tuple[dict[int, list[int]], list[list[int]]],
    part_one: bool = True,
) -> int:
    """Check the printing page ordering."""
    rules, updates = data

    total = 0
    for update in updates:
        result = None
        if check_update(rules, update):
            if part_one:
                result = update

        elif not part_one:
            result = fix_update(rules, update)

        if result:
            total += result[len(update) // 2]

    return total


def main() -> None:
    """Day tasks."""
    runner = Runner(
        5,
        check_page_order,
        load_parser=load_parser,
        extra_args_2=[False],
    )
    runner.part_1(143)
    runner.part_2(123)


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, RuntimeError):
        pass
