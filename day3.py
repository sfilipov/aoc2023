from typing import NamedTuple
from collections import defaultdict


class NumberRange(NamedTuple):
    number: int
    start: int
    end: int


class Position(NamedTuple):
    row: int
    column: int


def get_neighbours(row: int, start: int, end: int | None = None) -> list[Position]:
    if end is None:
        end = start

    neighbours = []
    for i in range(row - 1, row + 2):
        for j in range(start - 1, end + 2):
            if i == row and start <= j <= end:
                continue
            neighbours.append(Position(i, j))
    return neighbours


def get_numbers_for_positions(numbers: dict[int, list[NumberRange]], positions: list[Position]) -> list[NumberRange]:
    positions_per_row: defaultdict[int, list[Position]] = defaultdict(list)
    for pos in positions:
        positions_per_row[pos.row].append(pos)

    result = []
    for row, ppr in positions_per_row.items():
        for num_range in numbers[row]:
            if any(True for pos in ppr if num_range.start <= pos.column <= num_range.end):
                result.append(num_range)

    return result


def parse_lines(lines: list[str]):
    numbers: dict[int, list[NumberRange]] = defaultdict(list)
    all_symbols: set[Position] = set()
    star_symbols: set[Position] = set()
    for row, line in enumerate(lines):
        num_start, num_end = None, None
        for column, char in enumerate(line):
            if char.isdigit():
                if num_start is None:
                    num_start = column
                if column == len(line) - 1:
                    num_end = column
            else:
                if num_start is not None:
                    num_end = column - 1
                if char == '*':
                    all_symbols.add(Position(row=row, column=column))
                    star_symbols.add(Position(row=row, column=column))
                if char not in ('.', '*'):
                    all_symbols.add(Position(row=row, column=column))

            if num_start is not None and num_end is not None:
                number = int(line[num_start:num_end + 1])
                number_range = NumberRange(number, num_start, num_end)
                numbers[row].append(number_range)
                num_start, num_end = None, None

    return numbers, all_symbols, star_symbols


def main():
    with open('day3_input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    numbers, all_symbols, star_symbols = parse_lines(lines)

    result_part1 = 0
    for row, num_ranges in numbers.items():
        for num in num_ranges:
            neighbours = get_neighbours(row, num.start, num.end)
            has_symbol_neighbour = any(position in all_symbols for position in neighbours)
            if has_symbol_neighbour:
                result_part1 += num.number

    result_part2 = 0
    for star in star_symbols:
        neighbours = get_neighbours(star.row, star.column)
        nums = get_numbers_for_positions(numbers, neighbours)
        if len(nums) == 2:
            a, b = nums
            result_part2 += a.number * b.number

    print(result_part1)
    print(result_part2)


if __name__ == '__main__':
    main()
