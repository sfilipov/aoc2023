from copy import deepcopy
from hashlib import md5


CYCLES = 1_000_000_000


def transpose(rows):
    if not rows or not rows[0]:
        return rows

    n = len(rows)
    m = len(rows[0])
    result = []
    for j in range(m):
        col = []
        for i in range(n):
            col.append(rows[i][j])
        result.append("".join(col))

    return result


def tilt_row(row: str, reverse=False):
    if reverse:
        row = row[::-1]

    def tilt_free(row):
        n = len(row)
        if n < 2:
            return row
        if n == 2:
            a, b = row
            return f"{b}{a}" if a == "." and b == "O" else row

        middle = n // 2
        left = tilt_free(row[:middle])
        right = tilt_free(row[middle:])
        result = []
        i = 0
        j = 0
        while i < len(left) or j < len(right):
            if i == len(left):
                result.append(right[j])
                j += 1
                continue

            if j == len(right):
                result.append(left[i])
                i += 1
                continue

            if i < len(left) and left[i] == "O":
                result.append("O")
                i += 1
            else:
                result.append(right[j])
                j += 1

        return "".join(result)

    squares = []
    for i, char in enumerate(row):
        if char == "#":
            squares.append(i)

    prev = None
    result = []
    for square in squares:
        start, end = prev + 1 if prev is not None else 0, square
        result.append(tilt_free(row[start:end]))
        result.append("#")
        prev = square
    start = prev + 1 if prev is not None else 0
    result.append(tilt_free(row[start:]))
    result_row = "".join(result)
    if reverse:
        result_row = result_row[::-1]
    return result_row


def tilt_rows(rows, reverse=False):
    return [tilt_row(row, reverse=reverse) for row in rows]


def tilt_north(rows):
    rows = transpose(rows)
    rows = tilt_rows(rows)
    rows = transpose(rows)
    return rows


def tilt_south(rows):
    rows = transpose(rows)
    rows = tilt_rows(rows, reverse=True)
    rows = transpose(rows)
    return rows


def tilt_west(rows):
    return tilt_rows(rows)


def tilt_east(rows):
    return tilt_rows(rows, reverse=True)


def tilt_calculate_cycle(rows, cycles=1):
    seen = {}
    loads = {}
    prev = None
    next = None
    for i in range(cycles):
        rows = tilt_north(rows)
        rows = tilt_west(rows)
        rows = tilt_south(rows)
        rows = tilt_east(rows)
        h = hash_rows(rows)
        if h in seen:
            prev = seen[h]
            next = i
            break
        seen[h] = i
        loads[i] = calculate_load(rows)

    if prev and next:
        mod = next - prev
        mod_index = (cycles - prev - 1) % mod
        return loads[prev + mod_index]

    return loads[cycles - 1]


def calculate_load(rows):
    n = len(rows)
    result = 0
    for i, row in enumerate(rows):
        for char in row:
            if char == "O":
                result += n - i
    return result


def hash_rows(rows):
    return md5("\n".join(rows).encode()).digest()


def main():
    with open("day14_input.txt") as f:
        rows = [line.strip() for line in f.readlines()]

    rows = tilt_north(deepcopy(rows))
    print(calculate_load(rows))

    load = tilt_calculate_cycle(rows, CYCLES)
    print(load)


if __name__ == "__main__":
    main()
