def in_to_out(dir, symbol):
    if symbol == ".":
        return [dir]
    if symbol == "-":
        if dir in ("l", "r"):
            return [dir]
        else:
            return ["l", "r"]
    if symbol == "|":
        if dir in ("t", "b"):
            return [dir]
        else:
            return ["t", "b"]
    if symbol == "\\":
        mir_map = {
            "l": "t",
            "t": "l",
            "r": "b",
            "b": "r",
        }
        return [mir_map[dir]]
    if symbol == "/":
        mir_map = {
            "l": "b",
            "b": "l",
            "r": "t",
            "t": "r",
        }
        return [mir_map[dir]]
    return []


def next_for_ray(grid, dir, i, j):
    n = len(grid)
    m = len(grid[0])
    if dir == "l" and j < m - 1:
        return (dir, i, j + 1)
    if dir == "r" and j > 0:
        return (dir, i, j - 1)
    if dir == "t" and i < n - 1:
        return (dir, i + 1, j)
    if dir == "b" and i > 0:
        return (dir, i - 1, j)
    return None


def part1(grid):
    return calc_energized(grid, ("l", 0, 0))


def part2(grid):
    max_seen = 0
    n = len(grid)
    m = len(grid[0])

    for i in range(n):
        left = calc_energized(grid, ("l", i, 0))
        right = calc_energized(grid, ("r", i, m - 1))
        max_seen = max(max_seen, left, right)

    for j in range(m):
        top = calc_energized(grid, ("t", 0, j))
        bottom = calc_energized(grid, ("b", n - 1, j))
        max_seen = max(max_seen, top, bottom)

    return max_seen


def calc_energized(grid, start):
    rays_from: list[tuple[str, int, int]] = [start]
    rays_seen = {}
    while rays_from:
        dir, i, j = rays_from.pop()
        seen = rays_seen.setdefault((i, j), [])
        if dir in seen:
            continue
        else:
            seen.append(dir)

        symbol = grid[i][j]
        for out_dir in in_to_out(dir, symbol):
            next_ray = next_for_ray(grid, out_dir, i, j)
            if next_ray:
                rays_from.append(next_ray)

    return len(rays_seen)


def main():
    with open("day16_input.txt") as f:
        grid = [line.strip() for line in f.readlines()]

    print(part1(grid))
    print(part2(grid))


if __name__ == "__main__":
    main()
