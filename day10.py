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
    return conn_for_symbol(get_from_grid(grid, pos))


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
    if symbol == "S":
        conn = conn_for_start(grid, pos)
    else:
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


def traverse_furthest(grid: list[str], start: Position) -> int:
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
    return result


def main():
    with open("day10_input.txt") as f:
        grid = [line.strip() for line in f.readlines()]

    start = find_start(grid)
    result = traverse_furthest(grid, start)
    print(result)


if __name__ == "__main__":
    main()
