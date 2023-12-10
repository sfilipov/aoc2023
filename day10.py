from typing import NamedTuple
from collections import deque


class Position(NamedTuple):
    row: int
    col: int


def find_start(grid: list[str]) -> Position:
    for i, row in enumerate(grid):
        for j, symbol in enumerate(row):
            if symbol == "S":
                return Position(i, j)

    raise Exception("Start not found")


def conn_for_symbol(symbol: str) -> str:
    conns = {
        "|": "ns",
        "-": "ew",
        "L": "ne",
        "J": "nw",
        "7": "sw",
        "F": "se",
        ".": "",
        "S": "",
    }
    return conns[symbol]


def get_from_grid(grid: list[str], pos: Position) -> str:
    if not 0 <= pos.row < len(grid):
        return "."
    row = grid[pos.row]
    if not 0 <= pos.col < len(row):
        return "."
    return row[pos.col]


def conn_for_pos(grid: list[str], pos: Position) -> str:
    symbol = get_from_grid(grid, pos)
    return conn_for_symbol(symbol) if symbol != "S" else conn_for_start(grid, pos)


def conn_for_start(grid: list[str], pos: Position) -> str:
    conn = ""
    if "s" in conn_for_pos(grid, Position(pos.row - 1, pos.col)):
        conn += "n"
    if "n" in conn_for_pos(grid, Position(pos.row + 1, pos.col)):
        conn += "s"
    if "w" in conn_for_pos(grid, Position(pos.row, pos.col + 1)):
        conn += "e"
    if "e" in conn_for_pos(grid, Position(pos.row, pos.col - 1)):
        conn += "w"

    if len(conn) != 2:
        raise Exception("Expected 2 connections for start")

    return conn


def next_for_pos(grid: list[str], pos: Position) -> tuple[Position, Position]:
    symbol = grid[pos.row][pos.col]
    conn = conn_for_pos(grid, pos)

    result: list[Position] = []
    if "n" in conn:
        result.append(Position(pos.row - 1, pos.col))
    if "s" in conn:
        result.append(Position(pos.row + 1, pos.col))
    if "e" in conn:
        result.append(Position(pos.row, pos.col + 1))
    if "w" in conn:
        result.append(Position(pos.row, pos.col - 1))

    return (result[0], result[1])


def traverse_furthest(grid: list[str], start: Position) -> tuple[int, set[Position]]:
    dis = {start: 0}
    to_visit = deque(next_for_pos(grid, start))
    result = 0
    while len(to_visit):
        p = to_visit.popleft()
        if p in dis:
            continue
        left, right = next_for_pos(grid, p)
        if left in dis:
            dis[p] = dis[left] + 1
            to_visit.append(right)
        else:
            dis[p] = dis[right] + 1
            to_visit.append(left)
        result = max(result, dis[p])
    return (result, set(dis))


def count_inside(grid: list[str], loop_seen: set[Position]) -> int:
    def is_inside(pos: Position):
        intersects = 0
        loop_source = None
        for j in range(pos.col + 1, len(grid[pos.row])):
            ray = Position(pos.row, j)
            if ray not in loop_seen:
                continue
            conns = conn_for_pos(grid, ray)
            if not loop_source:
                if conns == "ns":
                    intersects += 1
                else:
                    loop_source = "n" if "n" in conns else "s"
            else:
                if conns == "ew":
                    continue
                if loop_source not in conns:
                    intersects += 1
                loop_source = None

        return intersects % 2 == 1

    count = 0
    for i, row in enumerate(grid):
        for j in range(len(row)):
            pos = Position(i, j)
            if pos in loop_seen:
                continue
            if is_inside(pos):
                count += 1

    return count


def main():
    with open("day10_input.txt") as f:
        grid = [line.strip() for line in f.readlines()]

    start = find_start(grid)
    result_part1, loop_seen = traverse_furthest(grid, start)
    result_part2 = count_inside(grid, loop_seen)

    print(result_part1)
    print(result_part2)


if __name__ == "__main__":
    main()
