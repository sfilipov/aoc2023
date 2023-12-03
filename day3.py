def is_symbol(char: str) -> bool:
    if char == '.':
        return False
    if char.isdigit():
        return False
    return True


def check_for_symbol(lines: list[str], row: int, col_start: int, col_end: int) -> bool:
    neighbours: list[str] = []
    if col_start > 0:
        if row > 0:
            neighbours.append(lines[row - 1][col_start - 1])
        neighbours.append(lines[row][col_start - 1])
        if row < len(lines) - 1:
            neighbours.append(lines[row + 1][col_start - 1])
    if col_end < len(lines[row]) - 1:
        if row > 0:
            neighbours.append(lines[row - 1][col_end + 1])
        neighbours.append(lines[row][col_end + 1])
        if row < len(lines) - 1:
            neighbours.append(lines[row + 1][col_end + 1])
    if row > 0:
        for char in lines[row - 1][col_start:col_end + 1]:
            neighbours.append(char)
    if row < len(lines) - 1:
        for char in lines[row + 1][col_start:col_end + 1]:
            neighbours.append(char)

    for char in neighbours:
        if char == '.':
            continue
        if char.isdigit():
            continue
        return True

    return False


def main():
    with open('day3_input.txt', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    result = 0
    for i, line in enumerate(lines):
        num_start = None
        for j, char in enumerate(line):
            if char.isdigit():
                if num_start is None:
                    num_start = j
                if j == len(line) - 1:
                    if check_for_symbol(lines, i, num_start, j):
                        result += int(line[num_start:j + 1])
            else:
                if num_start is not None and check_for_symbol(lines, i, num_start, j - 1):
                    result += int(line[num_start:j])
                num_start = None

    print(result)


if __name__ == '__main__':
    main()
